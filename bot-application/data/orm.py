import os
from MySQLdb import _mysql
from .core import tables


class Connection:
    def _fill_schema(self):
        self.connection.query('CREATE DATABASE IF NOT EXISTS toaster')
        self.connection.commit()

    def _fill_tables(self):
        self.connection.query('USE toaster')
        for table in tables:
            self.connection.query(table)

        self.connection.commit()

    def __init__(self, allow_debug_text=True):
        try:
            self.connection = _mysql.connect(
                host=os.getenv("SQL_HOST"),
                port=int(os.getenv("SQL_PORT")),
                user=os.getenv("SQL_USER"),
                password=os.getenv("SQL_PASSWORD")
            )

            if allow_debug_text:
                print("Произведено подключение к MySQL Server.")

            self._fill_schema()
            self._fill_tables()

        except Exception as error:
            if allow_debug_text:
                print("Ошибка при подключении к MySQL Server", error)


class BaseTable:
    _ops = {
        '__le': '<=',
        '__lt': '<',
        '__ge': '>=',
        '__gt': '>',
        '__nt': '!='
    }

    def _get_ratio(self, rows: dict) -> list:
        summary = []
        for key, value in rows.items():
            op = key[-4:-1]+key[-1]
            op = self._ops.get(op, '=')

            if op != '=':
                key = key[0:-4]

            summary.append(f"{key} {op} '{value}'")

        return summary

    def __init__(self, table_name, connection):
        self.table_name = table_name
        self.con = connection

    def select(self, fields: tuple = None, **rows):
        if fields:
            summary_fields = ', '.join(fields)
        else:
            summary_fields = '*'

        query = f"SELECT {summary_fields} FROM {self.table_name}"

        if rows:
            summary_rows = ' AND '.join(self._get_ratio(rows))
            query += f" WHERE {summary_rows}"

        self.con.query('USE toaster')
        self.con.query(query)
        return self.con.store_result().fetch_row()

    def insert(self, on_duplicate=None, **rows):
        if not rows:
            return

        summary_keys = ', '.join([key for key in rows.keys()])
        summary_values = ', '.join([f"'{value}'" for value in rows.values()])
        query = f"INSERT INTO {self.table_name} ({summary_keys}) VALUES ({summary_values})"

        if on_duplicate == "ignore":
            query += " ON DUPLICATE KEY UPDATE id=id"

        if on_duplicate == "update":
            query += f""" ON DUPLICATE KEY UPDATE """ \
                     f"""{', '.join([f"{key}='{value}'" for key, value in rows.items()])}"""

        self.con.query('USE toaster')
        self.con.query(query)
        self.con.commit()

    def update(self, new_data: dict, **rows):
        if not new_data:
            return

        summary_fields = ', '.join([f"{key}='{value}'" for key, value in new_data.items()])
        query = f"UPDATE {self.table_name} SET {summary_fields}"

        if rows:
            summary_rows = ' AND '.join(self._get_ratio(rows))
            query += f" WHERE {summary_rows}"

        self.con.query('USE toaster')
        self.con.query(query)
        self.con.commit()

    def delete(self, **rows):
        query = f"DELETE FROM {self.table_name}"

        if rows:
            summary_rows = ' AND '.join(self._get_ratio(rows))
            query += f" WHERE {summary_rows}"

        self.con.query('USE toaster')
        self.con.query(query)
        self.con.commit()


class DataBase:
    _base_table = BaseTable
    _tunnel = Connection()

    @property
    def conversations(self):
        return self._base_table(
            table_name="conversations",
            connection=self._tunnel.connection,
        )

    @property
    def settings(self):
        return self._base_table(
            table_name="settings",
            connection=self._tunnel.connection,
        )

    @property
    def permissions(self):
        return self._base_table(
            table_name="permissions",
            connection=self._tunnel.connection,
        )

    @property
    def kicked(self):
        return self._base_table(
            table_name="kicked",
            connection=self._tunnel.connection,
        )

    @property
    def banned(self):
        return self._base_table(
            table_name="banned",
            connection=self._tunnel.connection,
        )

    @property
    def warned(self):
        return self._base_table(
            table_name="warned",
            connection=self._tunnel.connection,
        )

    @property
    def muted(self):
        return self._base_table(
            table_name="muted",
            connection=self._tunnel.connection,
        )

    @property
    def queue(self):
        return self._base_table(
            table_name="queue",
            connection=self._tunnel.connection,
        )
