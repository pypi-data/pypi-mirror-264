
from sqlite_utils import hookimpl
import sqlite_utils_sqlite_hello

__version__ = "0.1.0a79"
__version_info__ = tuple(__version__.split("."))

@hookimpl
def prepare_connection(conn):
  conn.enable_load_extension(True)
  sqlite_utils_sqlite_hello.load(conn)
  conn.enable_load_extension(False)
