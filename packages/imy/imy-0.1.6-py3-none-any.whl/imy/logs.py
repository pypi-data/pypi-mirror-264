"""
Utilities for setting up Python's weirdo logging system. Including logging to
MongoDB if you feel crazy.
"""

from __future__ import annotations

import logging
import logging.handlers
import queue
import socket
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import *  # type: ignore

import uniserde
from bson import ObjectId
from uniserde import BsonDoc

from . import async_utils

try:
    import motor  # type: ignore
    import motor.motor_asyncio  # type: ignore
    import pymongo.collection
except ImportError:
    if TYPE_CHECKING:
        import motor  # type: ignore
        import motor.motor_asyncio  # type: ignore
        import pymongo.collection


__all__ = [
    "LogLevel",
    "MongoDbLogger",
    "setup_logging",
]


T = TypeVar("T")


LogLevel: TypeAlias = Literal["debug", "info", "warning", "error", "fatal"]
LOG_LEVEL_NAMES = get_args(LogLevel)

Environment: TypeAlias = Literal["development", "production"]


def _log_level_to_python(level: LogLevel) -> int:
    return getattr(logging, level.upper())


def _log_level_from_python(level: int) -> LogLevel:
    return logging.getLevelName(level).lower()


@dataclass
class LogEntry(uniserde.Serde):
    id: ObjectId
    timestamp: datetime
    environment: Environment
    host: str
    app: str
    level: LogLevel
    message: str
    payload: dict[str, Any]


class MongoDbLogger(logging.StreamHandler):
    """
    Logger, which stores its entries in a MongoDB database.

    Database access is asynchronous, and likely on another server. `await`ing
    every log operation would be incredibly slow. Instead, this logger only
    synchronously queues log entries, and then later asynchronously copies them
    to the database.
    """

    def __init__(
        self,
        collection: pymongo.collection.Collection,
        *,
        environment: Environment,
        app: str,
        host: str | None = None,
    ):
        super().__init__()

        self._sync_collection = collection

        self._host = socket.gethostname() if host is None else host
        self._environment: Environment = environment
        self._app = app

        self._last_log_writeback_time_montonic = time.monotonic()
        self._pending_log_entries: queue.Queue[LogEntry] = queue.Queue()

        self._writeback_thread = threading.Thread(
            target=self._writeback_worker, daemon=True
        )
        self._writeback_thread.start()

    def create_log_entries_sync(self, entries: Iterable[LogEntry]) -> None:
        """
        Batch creates new log entries in the database.

        The entries need to have unique ids among all entries in the database.
        This is not checked for performance reasons.
        """
        # MongoDB doesn't like empty inserts
        entry_data = [entry.as_bson() for entry in entries]

        if not entry_data:
            return

        # Insert the entries
        self._sync_collection.insert_many(entry_data)

    def flush_sync(self) -> None:
        """
        Copies any not yet stored log entries into the database.
        """
        # Move the log entries into a local variable
        in_flight_entries = []

        while True:
            try:
                in_flight_entries.append(self._pending_log_entries.get_nowait())
            except queue.Empty:
                break

        # Try to push the entries into the database
        try:
            self.create_log_entries_sync(in_flight_entries)

        # If the operation fails, put the entries back into the queue so they
        # can be retried later
        except Exception:
            for entry in in_flight_entries:
                self._pending_log_entries.put(entry)

            raise

    def _writeback_worker(self) -> None:
        # Keep copying entries forever. There is no need to return because the
        # thread is daemonized.
        #
        # TODO: What if the logger is deleted? This isn't currently supported.
        CYCLE_TIME = 10

        while True:
            # Wait some time before writing back. This batches log entries
            # together.
            now = time.monotonic()
            sleep_time = CYCLE_TIME - (now - self._last_log_writeback_time_montonic)

            if sleep_time > 0:
                time.sleep(sleep_time)

            # Copy the pending log entries into the database
            try:
                self.flush_sync()
            except Exception as e:
                logging.error(f"Error writing back log entries: {e}")

                # Wait a bit before retrying
                time.sleep(20)

            # Housekeeping
            self._last_log_writeback_time_montonic = time.monotonic()

    def queue_log(
        self,
        level: LogLevel,
        message: str,
        *,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """
        Creates a log entry and queues it for storage to the database. The entry
        will be created later, or once `flush` is called.
        """
        self._pending_log_entries.put(
            LogEntry(
                id=ObjectId(),
                timestamp=datetime.now(timezone.utc),
                environment=self._environment,
                host=self._host,
                app=self._app,
                level=level,
                message=message,
                payload={} if payload is None else payload,
            )
        )

    def emit(self, record: logging.LogRecord) -> None:
        """
        For compatibility with python's logging module.
        """

        self.queue_log(
            level=_log_level_from_python(record.levelno),
            message=record.message,
        )

    def find_log_entries(
        self,
        *,
        environment: Environment | None = None,
        levels: Iterable[LogLevel] | None = None,
        newer_than: datetime | None = None,
        older_than: datetime | None = None,
    ) -> AsyncIterable[LogEntry]:
        """
        Returns an async iterator over all log entries in the database matching
        the given filters.
        """
        # Build the query
        query: BsonDoc = {}

        if environment is not None:
            query["environment"] = uniserde.as_bson(environment)

        if levels is not None:
            query["level"] = {"$in": [uniserde.as_bson(level) for level in levels]}

        if newer_than is not None:
            query["timestamp"] = {"$gt": newer_than}

        if older_than is not None:
            query["timestamp"] = {"$lt": older_than}

        # Yield all matches
        def sync_iterator() -> Iterator[LogEntry]:
            cursor = self._sync_collection.find(query)

            for doc in cursor:
                yield LogEntry.from_bson(doc)

        return async_utils.iterator_to_thread(sync_iterator(), batch_size=50)

    def watch_log_entries(
        self,
        *,
        environment: Environment | None = None,
        levels: Iterable[LogLevel] | None = None,
    ) -> AsyncIterable[LogEntry]:
        """
        Returns an async iterator over all new log entries in the database
        matching the given filters.

        The iterator will block until new log entries are available.
        """
        # Build the filter pipeline
        query: BsonDoc = {"operationType": "insert"}

        if environment is not None:
            query["fullDocument.environment"] = uniserde.as_bson(environment)

        if levels is not None:
            query["fullDocument.level"] = {
                "$in": [uniserde.as_bson(level) for level in levels]
            }

        pipeline = [
            {
                "$match": query,
            }
        ]

        # Watch for changes
        def sync_iterator() -> Iterator[LogEntry]:
            for change in self._sync_collection.watch(pipeline=pipeline):
                yield LogEntry.from_bson(change["fullDocument"])

        return async_utils.iterator_to_thread(sync_iterator(), batch_size=1)


@overload
def setup_logging(
    *,
    info_log_path: Path,
    debug_log_path: Path,
    database_collection: None,
) -> MongoDbLogger:
    ...


@overload
def setup_logging(
    *,
    info_log_path: Path,
    debug_log_path: Path,
    database_collection: pymongo.collection.Collection,
    database_environment: Environment,
    database_host: str | None = None,
    database_app: str,
    database_log_level: LogLevel = "debug",
) -> MongoDbLogger:
    ...


def setup_logging(
    *,
    info_log_path: Path,
    debug_log_path: Path,
    database_collection: pymongo.collection.Collection | None,
    database_environment: Environment | None = None,
    database_host: str | None = None,
    database_app: str | None = None,
    database_log_level: LogLevel = "debug",
) -> MongoDbLogger | None:
    """
    Creates a nice logging setup.

    - INFO logs to `info_log_path`, keeping logs indefinitely
    - DEBUG logs to `stdout`
    - DEBUG logs to `debug_log_path`, keeping a limited number of days
    - DEBUG logs into the database

    Persistence loggers can lose some log entries if they are not flushed before
    closing the application. If every single entry is important to you, make
    sure to flush the returned persistence logger before ending the script.

    :param info_log_path: Path to the info log file
    :param debug_log_path: Path to the debug log file
    :param db: The persistence to store logs in
    :return: The created PersistenceLogger
    """

    root_logger = logging.getLogger("")
    root_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s")

    # Make sure the log directories exist
    info_log_path.parent.mkdir(parents=True, exist_ok=True)
    debug_log_path.parent.mkdir(parents=True, exist_ok=True)

    # Info -> file
    handler = logging.handlers.TimedRotatingFileHandler(
        info_log_path,
        encoding="utf-8",
        when="midnight",
        utc=True,
    )
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Debug -> stdout
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Debug -> file
    handler = logging.handlers.TimedRotatingFileHandler(
        debug_log_path,
        encoding="utf-8",
        when="midnight",
        utc=True,
        backupCount=7,
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Debug -> database
    if database_collection is None:
        pers_logger = None
    else:
        assert (
            database_environment is not None
        ), "Must provide an environment when logging to a database"

        assert (
            database_app is not None
        ), "Must provide an app name when logging to a database"

        pers_logger = MongoDbLogger(
            database_collection,
            host=database_host,
            environment=database_environment,
            app=database_app,
        )

        pers_logger.setLevel(_log_level_to_python(database_log_level))
        root_logger.addHandler(pers_logger)

    return pers_logger
