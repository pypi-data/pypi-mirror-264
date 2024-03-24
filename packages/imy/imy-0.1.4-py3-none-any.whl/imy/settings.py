"""
Utilities for loading settings from JSON files and environment variables.
"""

from __future__ import annotations

import enum
import os
from collections.abc import Iterable
from datetime import datetime, timedelta
from pathlib import Path
from typing import *  # type: ignore
from typing import Annotated, TypeVar

import introspection.typing
import json5
import uniserde
import uniserde.case_convert
from typing_extensions import dataclass_transform
from uniserde import Jsonable, ObjectId

__all__ = [
    "SettingsError",
    "LocalSetting",
    "Settings",
]


_DEFAULTS_BY_TYPE: dict[Type, Any] = {
    Any: None,
    bool: False,
    bytes: b"",
    datetime: datetime.now(),
    dict: {},
    enum.Enum: "",
    enum.Flag: [],
    float: 0.0,
    int: 0,
    list: [],
    Literal: "",
    set: set(),
    str: "",
    timedelta: timedelta(),
    tuple: tuple(),
    Union: None,
    ObjectId: "",
}  # type: ignore


class SettingsError(ValueError):
    """
    Raised when settings couldn't be loaded, for whichever reason.
    """

    pass


T = TypeVar("T")
LOCAL = object()
LocalSetting = Annotated[T, LOCAL]


@dataclass_transform()
class Settings:
    @classmethod
    def _get_fields(
        cls,
    ) -> tuple[Iterable[tuple[str, type]], Iterable[tuple[str, type]]]:
        """
        Returns iterators over all local and remote settings fields and their
        types.
        """
        local_fields: list[tuple[str, type]] = []
        remote_fields: list[tuple[str, type]] = []

        for attr_name, type_info in introspection.typing.get_type_annotations(
            cls
        ).items():
            if type_info.arguments:
                raw_type = introspection.typing.parameterize(
                    type_info.type, type_info.arguments
                )
            else:
                raw_type = type_info.type

            if LOCAL in type_info.annotations:
                attrs_list = local_fields
            else:
                attrs_list = remote_fields

            attrs_list.append((attr_name, raw_type))  # type: ignore

        return local_fields, remote_fields

    @staticmethod
    def _create_json_template(fields: Iterable[tuple[str, Type]]) -> str:
        """
        Create an empty JSON template for the provided fields.
        """

        # Build a JSON containing the default values for each field
        default_values_dict: dict[str, Jsonable] = {}

        for field_py_name, field_type in fields:
            field_doc_name = uniserde.case_convert.all_lower_to_camel_case(
                field_py_name
            )
            default_values_dict[field_doc_name] = _DEFAULTS_BY_TYPE.get(
                field_type, None
            )

        # Serialize the instance into formatted JSON
        serialized: str = json5.dumps(  # type: ignore
            default_values_dict,
            indent=4,
            quote_keys=True,
            trailing_commas=True,
        )

        # Add comments describing the fields
        serialized = serialized.strip()
        lines = serialized.splitlines()

        for ii, line in enumerate(lines[1:-1]):
            lines[ii] = "  // " + line.strip()

        # Done
        return "\n".join(lines) + "\n"

    @classmethod
    def _parse_fields(
        cls,
        *,
        fields: Iterable[tuple[str, Type]],
        values: Iterable[tuple[str, Any]],
        case_transform: Callable[[str], str],
        raise_on_superfluous: bool,
    ) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Parses the provided fields and values into a dictionary, transforming
        the field names using the provided `case_transform` function. The result
        is a tuple of two dictionaries: the first contains the parsed fields,
        the second any unparsed, i.e. superfluous values.

        ## Raises

        `SettingsError`: if any fields are missing, or of the wrong type.
        """
        # Prepare everything as dictionaries for quick lookup
        field_dict: dict[str, Type] = dict(fields)
        value_dict: dict[str, Any] = dict(values)

        # Parse the fields, popping them from the value dictionary
        parsed_fields: dict[str, Any] = {}

        for py_name, py_type in field_dict.items():
            doc_name = case_transform(py_name)

            try:
                raw_value = value_dict.pop(doc_name)
            except KeyError:
                raise SettingsError(f"The settings are missing the field `{doc_name}`")

            try:
                parsed_value = uniserde.from_json(raw_value, py_type)
            except uniserde.SerdeError as err:
                raise SettingsError(
                    f"`{raw_value}` is not a valid value for `{doc_name}`"
                ) from err

            parsed_fields[py_name] = parsed_value

        # Are superfluous values allowed?
        if raise_on_superfluous and value_dict:
            raise SettingsError(
                f"The settings contain superfluous fields: `{'`, `'.join(value_dict)}`"
            )

        # Done
        return parsed_fields, value_dict

    @staticmethod
    def _prepare_fields(
        local_fields: list[tuple[str, Type]],
        remote_fields: list[tuple[str, Type]],
        on_remote_fields: Literal["read-locally", "skip", "raise"],
    ) -> list[tuple[str, Type]]:
        """
        Normally, local fields are parsed locally, and remote fields remotely.
        However, it can be nice for testing purposes to treat remote fields as
        local.

        This function merges local fields and remote fields as chosen by
        `on_remote_fields`.

        If `on_remote_fields` is `read-locally`, the remote fields are treated
        as though they were local ones.

        If `on_remote_fields` is `skip`, the remote fields are ignored.

        If `on_remote_fields` is `raise`, an error is raised if any remote
        fields are present.

        The resulting local fields are returned.
        """
        # Read all fields locally, including remote ones
        if on_remote_fields == "read-locally":
            return local_fields + remote_fields

        # Skip over remote fields
        if on_remote_fields == "skip":
            return local_fields

        # Raise an error if remote fields are present
        assert on_remote_fields == "raise", on_remote_fields
        if remote_fields:
            remote_field_names = [field[0] for field in remote_fields]
            raise SettingsError(
                f"The class cannot be read locally, because it contains remote fields `{'`, `'.join(remote_field_names)}`"
            )

        # There is no remote fields
        return local_fields

    @classmethod
    def _load_from_values(
        cls,
        *,
        values: Iterable[tuple[str, Any]],
        case_transform: Callable[[str], str],
        on_remote_fields: Literal["read-locally", "skip", "raise"],
    ) -> Self:
        """
        Loads an instance of the settings from the provided values.

        If `on_remote_fields` is `read-locally`, the remote fields are treated as
        though they were local ones. `raise` raises an error if any remote
        fields are present, `skip` ignores them. Note that `skip` will result in
        an invalid instance - any remote fields won't be present, despite the
        type annotation.

        ## Raises

        `SettingsError`: if any fields are missing, superfluous or of the wrong
            type.
        """
        # Prepare the fields
        local_fields, remote_fields = cls._get_fields()
        effective_fields = cls._prepare_fields(
            local_fields=list(local_fields),
            remote_fields=list(remote_fields),
            on_remote_fields=on_remote_fields,
        )

        del local_fields, remote_fields

        # Parse the fields
        parsed_local, unparsed = cls._parse_fields(
            fields=effective_fields,
            values=values,
            case_transform=case_transform,
            raise_on_superfluous=True,
        )
        assert not unparsed, (
            unparsed,
            "Superfluous values present, despite them being disallowed?",
        )

        # Instantiate the class
        self = object.__new__(cls)

        for field_name, field_value in parsed_local.items():
            setattr(self, field_name, field_value)

        return self

    @classmethod
    def load_from_json(
        cls,
        source: Path | IO[str] | IO[bytes] | Jsonable,
        *,
        on_remote_fields: Literal["read-locally", "skip", "raise"] = "raise",
    ) -> Self:
        """
        Loads an instance of the settings from the provided JSON source. The
        source can either be a path to a file, an open file-like object, or the
        result of `json.parse`.

        Note that **strings are not treated as paths**, but rather as already
        parsed string values.

        If `source` is a `Path`, and the file doesn't exist, a template will be
        dumped to the location to help out the user.

        If `on_remote_fields` is `read-locally`, the remote fields are treated as
        though they were local ones. `raise` raises an error if any remote
        fields are present, `skip` ignores them. Note that `skip` will result in
        an invalid instance - any remote fields won't be present, despite the
        type annotation.

        ## Raises

        `SettingsError`: if any fields are missing, superfluous or of the wrong
            type.
        """

        # Load the JSON
        #
        # If a path was provided but doesn't exist, dump a template
        if isinstance(source, Path):
            try:
                with open(source, "r") as f:
                    raw_values = json5.load(f)

            except FileNotFoundError:
                source.parent.mkdir(parents=True, exist_ok=True)
                with open(source, "w") as f:
                    f.write(cls._create_json_template(cls._get_fields()[0]))

                raise SettingsError(
                    f"Could not find the settings file at `{source}`. A template has been created for you. Please fill out the values, then try again"
                )

            except ValueError as err:
                raise SettingsError(f"`{source}` is not a valid JSON file: {err}")

        # If the source is already parsed, use it as-is
        elif isinstance(source, (type(None), bool, int, float, str, tuple, list, dict)):
            raw_values = source

        # Read & parse file-like objects
        else:
            try:
                raw_values = json5.load(source)

            except ValueError as err:
                raise SettingsError(f"`{source}` is not valid JSON: {err}")

        # Make sure the JSON has parsed into a dictionary
        if not isinstance(raw_values, dict):
            raise SettingsError("The settings JSON must be a dictionary.")

        # Parse the values into an instance
        return cls._load_from_values(
            values=raw_values.items(),
            case_transform=uniserde.case_convert.all_lower_to_camel_case,
            on_remote_fields=on_remote_fields,
        )

    @classmethod
    def load_from_environment(
        cls,
        *,
        on_remote_fields: Literal["read-locally", "skip", "raise"] = "raise",
    ) -> Self:
        """
        Loads an instance of the settings from the provided JSON source. The
        source can either be a path to a file, an open file-like object, or the
        result of `json.parse`.

        Note that **strings are not treated as paths**, but rather as already
        parsed string values.

        If `on_remote_fields` is `read-locally`, the remote fields are treated as
        though they were local ones. `raise` raises an error if any remote
        fields are present, `skip` ignores them. Note that `skip` will result in
        an invalid instance - any remote fields won't be present, despite the
        type annotation.

        ## Raises

        `SettingsError`: if any fields are missing, superfluous or of the wrong
            type.
        """

        raise NotImplementedError("TODO: This function is entirely untested")

        # Prepare the fields
        local_fields, remote_fields = cls._get_fields()
        effective_fields = cls._prepare_fields(
            local_fields=list(local_fields),
            remote_fields=list(remote_fields),
            on_remote_fields=on_remote_fields,
        )

        del local_fields, remote_fields

        # Fetch all fields from the environment
        raw_values: dict[str, str] = {}

        for py_field_name, field_type in effective_fields:
            env_name = py_field_name.upper()

            try:
                raw_value = os.environ[env_name]
            except KeyError:
                raise SettingsError(
                    f"There is no environment variable set for `{env_name}`"
                )

            raw_values[env_name] = raw_value

        # Right now all values are strings. Parse them into something more
        # adequate using JSON.
        semi_parsed: dict[str, Any] = {}

        for py_field_name, raw_value in raw_values.items():
            # Keep strings as-is
            if field_type is str:
                semi_parsed[py_field_name] = raw_value
                continue

            # Otherwise drag them through the JSON parser
            try:
                semi_parsed[py_field_name] = json5.loads(raw_value)
            except ValueError as err:
                raise SettingsError(f"`{raw_value}` is not a valid value") from err

        # Parse the fields into an instance
        return cls._load_from_values(
            values=semi_parsed.items(),
            case_transform=str.upper,
            on_remote_fields=on_remote_fields,
        )
