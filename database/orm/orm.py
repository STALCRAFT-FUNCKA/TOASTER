import sqlite3
from database import sql_tables
from singltone import MetaSingleton


# ---------------------- Connection ----------------------- #
class Connection:
    filename = "database.db"

    def _fill_std_form(self):
        for table in sql_tables.tables:
            self.cursor.execute(table)

    def __init__(self, allow_debug_text=True, database_path=".\\{0}"):
        try:
            self.connection = sqlite3.connect(database_path.format(self.filename))
            self.cursor = self.connection.cursor()
            if allow_debug_text:
                print("База данных успешно подключена к SQLite")
                print(self)

            self._fill_std_form()

            self.cursor.execute('''PRAGMA foreign_keys=ON''')
            self.connection.commit()

        except sqlite3.Error as error:
            if allow_debug_text:
                print("Ошибка при подключении к SQLite", error)


# ------------------------ Tables ------------------------- #
class BaseTable:
    _ops = {
        '__le': '<=',
        '__lt': '<',
        '__ge': '>=',
        '__gt': '>'
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

    def __init__(self, table_name, cursor, connection):
        self.table_name = table_name
        self.con = connection
        self.cur = cursor

    def select(self, fields: tuple, **rows):
        summary_fields = ', '.join(fields)
        summary_rows = ' AND '.join(self._get_ratio(rows))
        query = f"SELECT ({summary_fields}) FROM {self.table_name} WHERE {summary_rows}"
        print(query)
        self.cur.execute(query)
        return self.cur.fetchall()

    def insert(self, **rows):
        summary_keys = ', '.join([key for key in rows.keys()])
        summary_values = ', '.join([f"'{value}'" for value in rows.values()])
        query = f"INSERT INTO {self.table_name} ({summary_keys}) VALUES ({summary_values})"
        print(query)
        self.cur.execute(query)
        self.con.commit()

    def update(self, new_data: dict, **rows):
        summary_fields = ', '.join([f"{key} = '{value}'" for key, value in new_data.items()])
        summary_rows = ' AND '.join(self._get_ratio(rows))
        query = f"UPDATE {self.table_name} SET {summary_fields} WHERE {summary_rows}"
        print(query)
        self.cur.execute(query)
        self.con.commit()

    def delete(self, **rows):
        summary_rows = ' AND '.join(self._get_ratio(rows))
        query = f"DELETE FROM {self.table_name} WHERE {summary_rows}"
        print(query)
        self.cur.execute(query)
        self.con.commit()


# ----------------------- MetaBase ------------------------ #

class DataBase(metaclass=MetaSingleton):
    _base_table = BaseTable
    _database_path = "..\\{0}"
    _tunnel = Connection(database_path="..\\{0}")

    @property
    def conversations(self):
        return self._base_table(
            table_name="conversations",
            connection=self._tunnel.connection,
            cursor=self._tunnel.cursor
        )

    @property
    def settings(self):
        return self._base_table(
            table_name="settings",
            connection=self._tunnel.connection,
            cursor=self._tunnel.cursor
        )

    @property
    def permissions(self):
        return self._base_table(
            table_name="permissions",
            connection=self._tunnel.connection,
            cursor=self._tunnel.cursor
        )

    @property
    def kicked(self):
        return self._base_table(
            table_name="kicked",
            connection=self._tunnel.connection,
            cursor=self._tunnel.cursor
        )

    @property
    def banned(self):
        return self._base_table(
            table_name="banned",
            connection=self._tunnel.connection,
            cursor=self._tunnel.cursor
        )

    @property
    def warned(self):
        return self._base_table(
            table_name="warned",
            connection=self._tunnel.connection,
            cursor=self._tunnel.cursor
        )

    @property
    def muted(self):
        return self._base_table(
            table_name="muted",
            connection=self._tunnel.connection,
            cursor=self._tunnel.cursor
        )

    @property
    def queue(self):
        return self._base_table(
            table_name="queue",
            connection=self._tunnel.connection,
            cursor=self._tunnel.cursor
        )


if __name__ == "__main__":
    database = DataBase()

