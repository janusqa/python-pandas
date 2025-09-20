import contextlib
import sqlite3 as database_driver
from collections.abc import Generator
from sqlite3 import Connection, Cursor
from sqlite3 import Error as DBError
from sqlite3 import OperationalError as DBOperationalError
from typing import Any


class DB:
    def __init__(self, database_dsn: dict[str, Any]) -> None:
        self.database_dsn = database_dsn

    @contextlib.contextmanager
    def connect(self) -> Generator[Cursor, None, None]:
        """
        Returns a Database Cursor that SQL Quries can be executed against.

        If connection is unsuccessful raise an error.

        - Commits if no exception occurs.
        - Rolls back if an exception occurs.
        - Closes the connection when done.
        """
        print("Connecting to database...")
        conn = None
        curr = None
        try:
            conn = database_driver.connect(**self.database_dsn)
            curr = conn.cursor()
            yield curr
            conn.commit()
        except (DBOperationalError, DBError) as error:
            if conn is not None:
                conn.rollback()
            error_msg = f"Database connection failed: {error}"
            raise RuntimeError(error_msg) from error
        finally:
            if curr is not None:
                curr.close()
            if conn is not None:
                conn.close()
            print("Database connection closed.")

    @contextlib.contextmanager
    def raw_connect(self) -> Generator[Cursor, None, None]:
        """
        Returns a raw Database Connection.

        If connection is unsuccessful raise an error.

        - Commits if no exception occurs.
        - Rolls back if an exception occurs.
        - Closes the connection when done.
        """
        print("Connecting to database...")
        conn = None
        try:
            conn = database_driver.connect(**self.database_dsn)
            yield conn
            conn.commit()
        except (DBOperationalError, DBError) as error:
            if conn is not None:
                conn.rollback()
            error_msg = f"Database connection failed: {error}"
            raise RuntimeError(error_msg) from error
        finally:
            if conn is not None:
                conn.close()
            print("Database connection closed.")

    def result_iter(
        self,
        cursor: Cursor,
        chunk_size: int = 1000,
    ) -> Generator[dict[str, Any], Any, None]:
        """An iterator that uses fetchmany to keep memory usage down."""
        if cursor.description is None:
            return

        column_names = [column_name[0] for column_name in cursor.description]

        while True:
            results = None
            if chunk_size == 0:
                results = cursor.fetchall()
            elif chunk_size == 1:
                results = cursor.fetchone()
            else:
                results = cursor.fetchmany(chunk_size)

            if not results:
                break

            if chunk_size == 1:
                yield {
                    column[0]: column[1]
                    for column in zip(column_names, results, strict=True)
                }
            else:
                for result in results:
                    yield {
                        column[0]: column[1]
                        for column in zip(column_names, result, strict=True)
                    }

    def enable_wal(self) -> None:
        with self.connect() as curr:
            try:
                curr.execute("""PRAGMA journal_mode""")
                result = next(self.result_iter(curr, 1))
                if result["journal_mode"] and result["journal_mode"].lower() != "wal":
                    print("set journal_mode=wal")
                    curr.execute("""PRAGMA journal_mode = WAL;""")
            except DBOperationalError as e:
                print(f"An error occurred during query execution: {e}")
