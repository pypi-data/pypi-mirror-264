from __future__ import annotations

import inspect
import io
from typing import *  # type: ignore

import introspection.typing
from typing_extensions import ParamSpec

__all__ = [
    "DependencyCycleError",
    "Injector",
    "get",
    "set",
    "bind",
]

T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")


class DependencyCycleError(Exception):
    def __init__(self, sequence: Sequence[Type]) -> None:
        super().__init__()
        self._sequence = sequence

    def __str__(self) -> str:
        f = io.StringIO()

        f.write(f"<{self.__class__.__name__} ")
        f.write(" -> ".join(key.__name__ for key in self._sequence))
        f.write(">")

        return f.getvalue()


def _parse_factory(factory: Callable) -> tuple[list[Type], Type]:
    """
    Given a factory function, return a tuple containing the set of types it
    depends on and the type of item generated. The types are extracted from the
    factory's signature and order is preserved.
    """
    signature = inspect.signature(factory)

    # TODO: What if the factory uses kwargs?

    # Parameters
    parameter_types: list[Type] = []

    for parameter in signature.parameters.values():
        # Make sure the parameter has a type annotation
        if parameter.annotation is parameter.empty:
            raise ValueError(
                f"All parameters of factory functions need to have type annotations. `{parameter.name}` is missing one."
            )

        # Return type
        info = introspection.typing.TypeInfo(parameter.annotation)
        parameter_types.append(info.type)  # type: ignore

    # Return type
    return_type = signature.return_annotation

    if return_type is signature.empty:
        raise ValueError("Factory functions need to have a return type annotation.")

    if return_type is None:
        raise ValueError("Factory functions must return a value.")

    if not inspect.isclass(return_type):
        raise ValueError("Factory functions must return a class.")

    # Done
    return parameter_types, return_type


class Injector:
    def __init__(
        self,
        *,
        items: Iterable[Any] = [],
        item_factories: Iterable[Callable] = [],
    ) -> None:
        # Keeps track of all components currently attached to the injector
        self._components: dict[Type, Any] = {type(item): item for item in items}

        # Factories can be used to create items if they are not already
        # available in the injector. Each factory may depend on any number of
        # other items and returns the newly created item.
        self._factories: dict[Type, tuple[list[Type], Callable]] = {}

        for factory in item_factories:
            types, item_type = _parse_factory(factory)
            self._factories[item_type] = (types, factory)

    def _get(
        self,
        key: Type[T],
        *,
        in_flight: list[Type[T]],
    ) -> T:
        """
        Helper function for `__getitem__`.
        """
        # If the item is already available in this injector, just return it
        try:
            return self._components[key]
        except KeyError:
            pass

        # If an item of this type is currently being constructed, there's a
        # dependency cycle. Report it.
        if key in in_flight:
            raise DependencyCycleError(in_flight + [key])

        # Try to find a factory that can create the item
        try:
            factory_param_types, factory = self._factories[key]
        except KeyError:
            raise KeyError(key)

        # Get all of the factory's dependencies
        factory_args: list[Any] = []

        for param_type in factory_param_types:
            factory_args.append(
                self._get(
                    param_type,
                    in_flight=in_flight + [key],
                )
            )

        # Create the item, register it and return
        item = factory(*factory_args)
        self._components[key] = item

        return item

    def __getitem__(self, key: Type[T]) -> T:
        """
        Given an item type, return the component of that type.

        ## Raises

        `KeyError`: If no item of the given type is available in this injector.

        `DependencyCycleError`: If the item cannot be constructed due to a
            dependency cycle.
        """
        # Delegate to the helper function
        return self._get(
            key,
            in_flight=[],
        )

    def __setitem__(self, item_type: Type[T], item: T) -> None:
        """
        Adds the given item to the injector. If the item is already present, it
        will be replaced.

        ## Raises

        `ValueError`: If the item is not an instance of the given type.
        """
        # Make sure the item is of the correct type
        if not isinstance(item, item_type):
            raise ValueError(
                f"Item has to be of type `{item_type}`, not `{type(item)}`"
            )

        # Add the item to the injector
        self._components[item_type] = item

    def bind(
        self,
        type: Type | None = None,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        """
        Adds the decorated function to the injector as a factory. The function's
        result must be in instance of the given type or subclass thereof.

        ## Raises

        `ValueError`: If the function's return type is not a subclass of the given
            type.
        """

        def decorator(func: Callable[P, R]) -> Callable[P, R]:
            # Parse the factory
            param_types, return_type = _parse_factory(func)
            key_type = return_type if type is None else type

            # Make sure the factory indeed returns the correct type
            if type is not None and not issubclass(return_type, type):
                raise ValueError(
                    f"The factory has to return values of type `{type}` (or any subclass), not `{return_type}`"
                )

            # Register the factory
            self._factories[key_type] = (param_types, func)
            return func

        return decorator


# Expose a global injector
GLOBAL_INJECTOR = Injector()

get = GLOBAL_INJECTOR.__getitem__
set = GLOBAL_INJECTOR.__setitem__
bind = GLOBAL_INJECTOR.bind
