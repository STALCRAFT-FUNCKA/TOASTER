import sqlite3
from typing import List

from DataBase import tables


class Connection:
    def _fill_std_form(self):
        for table in tables.tables:
            self.cursor.execute(table)

    """
    --------------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, filename, allow_debug_text=False):
        try:
            self.connection = sqlite3.connect(filename)
            self.cursor = self.connection.cursor()
            if allow_debug_text:
                print("База данных успешно подключена к SQLite")

            self._fill_std_form()

            self.cursor.execute('''PRAGMA foreign_keys=ON''')
            self.connection.commit()

        except sqlite3.Error as error:
            if allow_debug_text:
                print("Ошибка при подключении к SQLite", error)

    """
     --------------------------------------------------------------------------------------------------------------------
    """

    def version(self):
        self.cursor.execute("select sqlite_version();")
        record = self.cursor.fetchall()
        return record

    def debug(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        record = self.cursor.fetchall()
        print('Таблицы:', record)
        self.cursor.execute("SELECT peer_id, peer_name FROM conversations;")
        record = self.cursor.fetchall()
        print('Беседы:', record)

    """
    --------------------------------------------------------------------------------------------------------------------
    """

    def add_conversation(self, peer_id, peer_name, destination):
        request = f"""INSERT INTO conversations 
                        (
                            peer_id, 
                            peer_name,
                            destination
                        ) 
                        VALUES 
                        (
                            {peer_id}, 
                            '{peer_name}',
                            '{destination}'
                        );"""
        self.cursor.execute(request)
        self.connection.commit()

    def remove_conversation(self, peer_id):
        request = f"""DELETE FROM conversations WHERE peer_id = {peer_id};"""
        self.cursor.execute(request)
        self.connection.commit()

    def get_conversation(self, peer_id, destination) -> List[int]:
        if peer_id == -1:
            request = f"""SELECT peer_id FROM conversations WHERE destination = '{destination}'"""
        else:
            request = f"""SELECT peer_id FROM conversations WHERE peer_id = {peer_id} AND destination = '{destination}'"""

        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return [x[0] for x in record]
        else:
            return []

    """
    --------------------------------------------------------------------------------------------------------------------
    """

    def add_setting(self, peer_id, setting_name, setting_status):
        request = f"""INSERT INTO settings 
                        (
                            peer_id,
                            setting_name, 
                            setting_status
                        ) 
                        VALUES 
                        (   
                            {peer_id}, 
                            '{setting_name}', 
                            '{setting_status}' 
                        );"""
        self.cursor.execute(request)
        self.connection.commit()

    def get_setting(self, peer_id, setting_name) -> bool:
        request = f"""SELECT setting_status FROM settings WHERE setting_name = %s AND peer_id = %s"""
        self.cursor.execute(request, (setting_name, peer_id))
        record = self.cursor.fetchone()

        if record:
            return record[0]

        return False

    """
     --------------------------------------------------------------------------------------------------------------------
    """

    def set_permission(self, peer_id, user_id, user_name, user_url, permission_lvl, permission_name):
        request = ""
        if permission_lvl < 1:
            request = f"""DELETE FROM permissions WHERE user_id = {user_id} AND peer_id = {peer_id};"""

        elif permission_lvl < 3:
            request = f"""INSERT INTO permissions
                        (
                            peer_id,
                            user_id,
                            user_name,
                            user_url,
                            permission_lvl,
                            permission_name
                        )
                        VALUES 
                        (
                            {peer_id},
                            {user_id},
                            '{user_name}',
                            '{user_url}',
                            {permission_lvl},
                            '{permission_name}'
                        );"""

        self.cursor.execute(request)
        self.connection.commit()

    def get_permission(self, peer_id, user_id) -> int:
        request = f"""SELECT permission_lvl FROM permissions WHERE peer_id = {peer_id} AND user_id = {user_id};"""
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return record[0][0]

        else:
            return 0

    """
     --------------------------------------------------------------------------------------------------------------------
    """

    def add_kick(self, peer_id, user_id, user_name, user_url,
                 kicked_by_id, kicked_by_name, kicked_by_url, kick_time):
        request = f"""INSERT INTO kicked 
                        (
                            peer_id,
                            user_id, 
                            user_name, 
                            user_url, 
                            kicked_by_id, 
                            kicked_by_name, 
                            kicked_by_url, 
                            kick_time
                        ) 
                        VALUES 
                        (
                            {peer_id}, 
                            {user_id}, 
                            '{user_name}', 
                            '{user_url}', 
                            {kicked_by_id}, 
                            '{kicked_by_name}', 
                            '{kicked_by_url}', 
                            {kick_time}
                        );"""
        self.cursor.execute(request)
        self.connection.commit()

    def get_kick(self, peer_id, user_id) -> List[int]:
        request = f"""SELECT user_id FROM kicked WHERE peer_id = {peer_id} AND user_id = {user_id};"""
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return [x[0] for x in record]

        else:
            return []

    """
     --------------------------------------------------------------------------------------------------------------------
    """

    def add_ban(self, peer_id, user_id, user_name, user_url, banned_by_id, banned_by_name, banned_by_url, ban_time,
                unban_time):
        request = f"""INSERT INTO banned 
                        (
                            peer_id, 
                            user_id, 
                            user_name, 
                            user_url, 
                            banned_by_id, 
                            banned_by_name, 
                            banned_by_url, 
                            ban_time, 
                            unban_time
                        ) 
                        VALUES 
                        (
                            {peer_id}, 
                            {user_id}, 
                            '{user_name}', 
                            '{user_url}', 
                            {banned_by_id}, 
                            '{banned_by_name}', 
                            '{banned_by_url}', 
                            {ban_time},
                            {unban_time}
                        );"""
        self.cursor.execute(request)
        self.connection.commit()

    def remove_ban(self, peer_id, user_id):
        request = f"""DELETE FROM banned WHERE peer_id = {peer_id} AND user_id = {user_id};"""
        self.cursor.execute(request)
        self.connection.commit()

    def get_ban(self, peer_id, user_id) -> List[int]:
        request = f"""SELECT user_id FROM banned WHERE peer_id = {peer_id} AND user_id = {user_id};"""
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return [x[0] for x in record]

        else:
            return []

    """
     --------------------------------------------------------------------------------------------------------------------
    """

    def add_mute(self, peer_id, user_id, user_name, user_url, muted_by_id, muted_by_name, muted_by_url, mute_time,
                 unmute_time):
        request = f"""INSERT INTO muted 
                        (
                            peer_id, 
                            user_id, 
                            user_name, 
                            user_url, 
                            muted_by_id, 
                            muted_by_name, 
                            muted_by_url, 
                            mute_time, 
                            unmute_time
                        ) 
                        VALUES 
                        (
                            {peer_id}, 
                            {user_id}, 
                            '{user_name}', 
                            '{user_url}', 
                            {muted_by_id}, 
                            '{muted_by_name}', 
                            '{muted_by_url}', 
                            {mute_time}, 
                            {unmute_time}
                        );"""
        self.cursor.execute(request)
        self.connection.commit()

    def remove_mute(self, peer_id, user_id):
        request = f"""DELETE FROM muted WHERE peer_id = {peer_id} AND user_id = {user_id};"""
        self.cursor.execute(request)
        self.connection.commit()

    def get_mute(self, peer_id, user_id) -> List[int]:
        request = f"""SELECT user_id FROM muted WHERE peer_id = {peer_id} AND user_id = {user_id};"""
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return [x[0] for x in record]

        else:
            return []

    """
     --------------------------------------------------------------------------------------------------------------------
    """

    def add_warn(self, peer_id, user_id, user_name, user_url,
                 warned_by_id, warned_by_name, warned_by_url, warn_time, unwarn_time, warn_count):
        request = f"""INSERT INTO warned 
                        (
                            peer_id, 
                            user_id, 
                            user_name, 
                            user_url, 
                            warned_by_id, 
                            warned_by_name, 
                            warned_by_url, 
                            warn_time, 
                            unwarn_time,
                            warn_count
                        ) 
                        VALUES 
                        (
                            {peer_id}, 
                            {user_id}, 
                            '{user_name}', 
                            '{user_url}', 
                            {warned_by_id}, 
                            '{warned_by_name}', 
                            '{warned_by_url}', 
                            {warn_time}, 
                            {unwarn_time},
                            {warn_count}
                        );"""
        self.cursor.execute(request)
        self.connection.commit()
        # TODO: Сдилать првоерку на кол-во варнов

    def remove_warn(self, peer_id, user_id):
        request = f"""DELETE FROM warned WHERE peer_id = {peer_id} AND user_id = {user_id};"""
        self.cursor.execute(request)
        self.connection.commit()
        # TODO: Сделать проверку на кол-во варнов

    def get_warn(self, peer_id, user_id) -> int:
        request = f"""SELECT warn_count FROM warned WHERE peer_id = {peer_id} AND user_id = {user_id};"""
        self.cursor.execute(request)
        record = self.cursor.fetchone()

        if record:
            return record[0]

        return 0

    """
     --------------------------------------------------------------------------------------------------------------------
    """


if __name__ == "__main__":
    database = Connection('database.db')
    print(database.version())
    database.debug()
    print(database.get_setting(peer_id=2000000002, setting_name="Allow_Picture"))
