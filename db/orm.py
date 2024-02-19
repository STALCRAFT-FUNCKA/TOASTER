"""
This file contains a database connection class and
an object relational model for interacting with it.
"""
import os
import MySQLdb
from tools import MetaSingleton
from .core import tables


class Connection:
    """This class provides connection
    to the MySQL database.
    """
    def __init__(self, allow_debug_text=True):
        try:
            self._connection = MySQLdb.connect(
                host=os.getenv("SQL_HOST"),
                port=int(os.getenv("SQL_PORT")),
                user=os.getenv("SQL_USER"),
                password=os.getenv("SQL_PASSWORD")
            )
            self._connection.autocommit(True)
            self._cursor = self._connection.cursor()

            if allow_debug_text:
                print("Произведено подключение к MySQL Server.")

            self._fill_schema()
            self._fill_tables()

        except MySQLdb.Error as error:
            if allow_debug_text:
                print("Ошибка при подключении к MySQL Server", error)


    def _fill_schema(self):
        """Creates a schema named "toaster"
        if one does not exist.
        """
        self._cursor.execute('CREATE DATABASE IF NOT EXISTS toaster')


    def _fill_tables(self):
        """Populates the database with
        a standard table structure.
        """
        self._cursor.execute('USE toaster')
        for table in tables:
            self._cursor.execute(table)


    @property
    def cursor(self):
        """Returns database cursor object.
        """
        return self._cursor


    @property
    def connection(self):
        """Returns database connection object.
        """
        return self._connection



class BaseTable:
    """Defines the base object of the table in object-relative
    representation and the main methods of interaction with it.
    """
    def __init__(self, table_name, connection, cursor):
        self.table_name = table_name
        self.con = connection
        self.cur = cursor


    def raw(self, query: str):
        """Executing a raw query.

        Args:
            query (str): Raw SQL query.

        Returns:
            tuple: Tuple of rows.
        """
        self.cur.execute('USE toaster;')
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result if result else None



class DataBase(metaclass=MetaSingleton):
    """The main class is the database view.
    Organizes a connection and implements
    access to table properties using
    object-relational methods of the base table.
    """
    _base_table = BaseTable
    _tunnel = Connection()

    # TODO: add normal tables later
    @property
    def table(self):
        """A table property that implements
        object-relational access to the conversion table.
        """
        return self._base_table(
            table_name="table",
            connection=self._tunnel.connection,
            cursor=self._tunnel.cursor
        )
