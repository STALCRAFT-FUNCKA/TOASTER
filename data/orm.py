"""
This file contains a database connection class and
an object relational model for interacting with it.
"""

import os
import logging
import MySQLdb
from singltone import MetaSingleton
from .core import tables


class Connection:
    """
    This class provides connection to the MySQL database.
    """

    def _fill_schema(self):
        """
        Creates a database named "toaster" if one does not exist.
        """
        self._cursor.execute('CREATE DATABASE IF NOT EXISTS toaster')
        self._connection.commit()

    def _fill_tables(self):
        """
        Populates the database with a standard table structure.
        """
        self._cursor.execute('USE toaster')
        for table in tables:
            self._cursor.execute(table)

        self._connection.commit()

    def __init__(self, allow_debug_text=True):
        try:
            self._connection = MySQLdb.connect(
                host=os.getenv("SQL_HOST"),
                port=int(os.getenv("SQL_PORT")),
                user=os.getenv("SQL_USER"),
                password=os.getenv("SQL_PASSWORD")
            )
            self._cursor = self._connection.cursor()

            if allow_debug_text:
                print("Произведено подключение к MySQL Server.")

            self._fill_schema()
            self._fill_tables()

        except MySQLdb.Error as error:
            if allow_debug_text:
                print("Ошибка при подключении к MySQL Server", error)

    def get_cursor(self):
        """
        Returns database cursor object.
        """
        return self._cursor

    def get_connection(self):
        """
        Returns database connection object.
        """
        return self._connection


class BaseTable:
    """
    Defines the base object of the table in object-relative
    representation and the main methods of interaction with it.
    """
    _ops = {
        '__le': '<=',
        '__lt': '<',
        '__ge': '>=',
        '__gt': '>',
        '__nt': '!='
    }

    def _get_ratio(self, rows: dict) -> list:
        """
        When specifying a method for comparing variables in an ORM query method,
        you must use keywords. Key characters are transformed by this
        method into comparison operators. The function returns a list
        of strings that are arranged according to the desired pattern.

        Args:
            rows (dict): rows with transformation keys into comparison operators

        Returns:
            list: list of args with sql somprassion operators.
        """
        summary = []
        for key, value in rows.items():
            op = key[-4:-1]+key[-1]
            op = self._ops.get(op, '=')

            if op != '=':
                key = key[0:-4]

            summary.append(f"{key} {op} '{value}'")

        return summary

    def __init__(self, table_name, connection, cursor):
        self.table_name = table_name
        self.con = connection
        self.cur = cursor

    def select(self, fields: tuple = None, **rows):
        """
        Accepts arguments for fields, comparisons, etc., 
        forms a database select query from them and returns the result of its execution.
        Keys that mimic comparison operators:
            1) __le -> <= \n
            2) __lt -> <  \n
            3) __ge -> >= \n
            4) __gt -> >  \n
            5) __nt -> != \n

        Example rows:
            id__lt=10 -> id<10

        Args:
            fields (tuple, optional): Fields for which it is necessary to obtain data
            in the database. Defaults to None.

        Returns:
            str: MySQL query string.
        """
        if fields:
            summary_fields = ', '.join(fields)
        else:
            summary_fields = '*'

        query = f"SELECT {summary_fields} FROM {self.table_name}"

        if rows:
            summary_rows = ' AND '.join(self._get_ratio(rows))
            query += f" WHERE {summary_rows}"

        query += ";"

        self.cur.execute('USE toaster;')
        self.cur.execute(query)
        result = self.cur.fetchall()
        self.con.commit()
        logging.debug("Query: %s", query)
        logging.debug("Result: %s", result)
        return result

    def insert(self, on_duplicate=None, **rows):
        """
        Takes arguments for fields, comparisons, etc., 
        forms a database insert query from them and inserts data when it is executed.

        Args:
            on_duplicate (str, optional): On duplicate action. 
            Can be "ignore" or "update". Defaults to None.
        """
        if not rows:
            return

        summary_keys = ', '.join(rows.keys())  # Might be incorrect
        summary_values = ', '.join([f"'{value}'" for value in rows.values()])
        query = f""" INSERT INTO {self.table_name} ({summary_keys})
                     VALUES ({summary_values})
                """

        if on_duplicate == "ignore":
            query += " ON DUPLICATE KEY UPDATE id=id"

        if on_duplicate == "update":
            query += f""" ON DUPLICATE KEY UPDATE {', '.join(
                            [f"{key}='{value}'" for key, value in rows.items()]
                        )}
                     """

        query += ";"

        self.cur.execute('USE toaster;')
        self.cur.execute(query)
        self.con.commit()
        logging.debug("Query: %s", query)
        logging.debug("Result: executed")

    def update(self, new_data: dict, **rows):
        """
        Accepts arguments for fields, comparisons, etc.,
        forms a query from them to update the database
        and updates the data according to the dictionary
        of correspondences received as input when executing the request.
        Keys that mimic comparison operators:
            1) __le -> <= \n
            2) __lt -> <  \n
            3) __ge -> >= \n
            4) __gt -> >  \n
            5) __nt -> != \n

        Example rows:
            id__lt=10 -> id<10

        Args:
            new_data (dict): Dict of correspondences for replacing variable values.
        """
        if not new_data:
            return

        summary_fields = ', '.join(
            [f"{key}='{value}'" for key, value in new_data.items()])
        query = f"UPDATE {self.table_name} SET {summary_fields}"

        if rows:
            summary_rows = ' AND '.join(self._get_ratio(rows))
            query += f" WHERE {summary_rows}"

        query += ";"

        self.cur.execute('USE toaster;')
        self.cur.execute(query)
        self.con.commit()
        logging.debug("Query: %s", query)
        logging.debug("Result: executed")

    def delete(self, **rows):
        """
        Takes arguments for fields, comparisons, etc.,
        forms a request from them to delete from the
        database and deletes data according to the
        conditions specified by the comparison operators.
        Keys that mimic comparison operators:
            1) __le -> <= \n
            2) __lt -> <  \n
            3) __ge -> >= \n
            4) __gt -> >  \n
            5) __nt -> != \n

        Example rows:
            id__lt=10 -> id<10
        """
        query = f"DELETE FROM {self.table_name}"

        if rows:
            summary_rows = ' AND '.join(self._get_ratio(rows))
            query += f" WHERE {summary_rows}"

        query += ";"

        self.cur.execute('USE toaster;')
        self.cur.execute(query)
        self.con.commit()
        logging.debug("Query: %s", query)
        logging.debug("Result: executed")


class DataBase(metaclass=MetaSingleton):
    """
    The main class is the database view.
    Organizes a connection and implements
    access to table properties using
    object-relational methods of the base table.
    """
    _base_table = BaseTable
    _tunnel = Connection()

    @property
    def conversations(self):
        """
        A table property that implements
        object-relational access to the conversion table.
        """
        return self._base_table(
            table_name="conversations",
            connection=self._tunnel.get_connection(),
            cursor=self._tunnel.get_cursor()
        )

    @property
    def settings(self):
        """
        A table property that implements
        object-relational access to the settings table.
        """
        return self._base_table(
            table_name="settings",
            connection=self._tunnel.get_connection(),
            cursor=self._tunnel.get_cursor()
        )

    @property
    def permissions(self):
        """
        A table property that implements
        object-relational access to the permissions table.
        """
        return self._base_table(
            table_name="permissions",
            connection=self._tunnel.get_connection(),
            cursor=self._tunnel.get_cursor()
        )

    @property
    def kicked(self):
        """
        A table property that implements
        object-relational access to the kicked table.
        """
        return self._base_table(
            table_name="kicked",
            connection=self._tunnel.get_connection(),
            cursor=self._tunnel.get_cursor()
        )

    @property
    def banned(self):
        """
        A table property that implements
        object-relational access to the banned table.
        """
        return self._base_table(
            table_name="banned",
            connection=self._tunnel.get_connection(),
            cursor=self._tunnel.get_cursor()
        )

    @property
    def warned(self):
        """
        A table property that implements
        object-relational access to the warned table.
        """
        return self._base_table(
            table_name="warned",
            connection=self._tunnel.get_connection(),
            cursor=self._tunnel.get_cursor()
        )

    @property
    def muted(self):
        """
        A table property that implements
        object-relational access to the muted table.
        """
        return self._base_table(
            table_name="muted",
            connection=self._tunnel.get_connection(),
            cursor=self._tunnel.get_cursor()
        )

    @property
    def queue(self):
        """
        A table property that implements
        object-relational access to the queue table.
        """
        return self._base_table(
            table_name="queue",
            connection=self._tunnel.get_connection(),
            cursor=self._tunnel.get_cursor()
        )
