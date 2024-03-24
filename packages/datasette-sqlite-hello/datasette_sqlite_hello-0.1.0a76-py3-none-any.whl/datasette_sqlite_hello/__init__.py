
from datasette import hookimpl
import datasette_sqlite_hello

__version__ = "0.1.0a76"
__version_info__ = tuple(__version__.split("."))

@hookimpl
def prepare_connection(conn):
  conn.enable_load_extension(True)
  datasette_sqlite_hello.load(conn)
  conn.enable_load_extension(False)
