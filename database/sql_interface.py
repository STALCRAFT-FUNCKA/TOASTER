import sqlite3
from typing import List, Dict
from database import sql_tables
from singltone import MetaSingleton


class Connection(metaclass=MetaSingleton):
    def _fill_std_form(self):
        for table in sql_tables.tables:
            self.cursor.execute(table)

    """
    --------------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, filename, allow_debug_text=True):
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
        self.cursor.execute("SELECT peer_id, _get_peer_name FROM conversations;")
        record = self.cursor.fetchall()
        print('Беседы:', record)

    """
    --------------------------------------------------------------------------------------------------------------------
    """

    def add_conversation(self, data: Dict):
        request = f"""
            INSERT INTO 
                conversations 
                (
                    peer_id, 
                    peer_name,
                    destination
                ) 
            VALUES 
                (
                    {data.get("peer_id")}, 
                    '{data.get("peer_name")}',
                    '{data.get("peer_destination")}'
                );
        """
        self.cursor.execute(request)
        self.connection.commit()

    def remove_conversation(self, peer_id):
        request = f"""
            DELETE FROM 
                conversations 
            WHERE 
                peer_id = {peer_id};
        """
        self.cursor.execute(request)
        self.connection.commit()

    def get_conversation(self, peer_id, destination) -> List[int]:
        if peer_id == -1:
            request = f"""
                SELECT 
                    peer_id 
                FROM 
                    conversations 
                WHERE 
                    destination = '{destination}';
        """
        else:
            request = f"""
                SELECT 
                    peer_id 
                FROM 
                    conversations 
                WHERE 
                    peer_id = {peer_id} 
                AND 
                    destination = '{destination}';
            """

        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return [x[0] for x in record]
        else:
            return []

    """
    --------------------------------------------------------------------------------------------------------------------
    """

    def add_setting(self, data: Dict, setting_name, setting_status):
        request = f"""
            INSERT INTO 
                settings 
                (
                    peer_id,
                    setting_name, 
                    setting_status
                ) 
            VALUES 
                (   
                    {data.get("peer_id")}, 
                    '{setting_name}', 
                    '{setting_status}' 
                );
        """
        self.cursor.execute(request)
        self.connection.commit()

    def get_setting(self, peer_id, setting_name):
        request = f"""
            SELECT 
                setting_status 
            FROM 
                settings 
            WHERE 
                setting_name = '{setting_name}' 
            AND 
                peer_id = {peer_id};
        """
        self.cursor.execute(request)
        record = self.cursor.fetchone()

        if record:
            return True if record[0] == "True" else False

        return None

    """
     --------------------------------------------------------------------------------------------------------------------
    """

    def set_permission(self, data: Dict):
        request = ""
        if data.get("target_set_role") < 1:
            request = f"""
                DELETE FROM 
                    permissions 
                WHERE 
                    user_id = {data.get("target_id")} 
                AND 
                    peer_id = {data.get("peer_id")};
            """

        elif data.get("target_set_role") < 3:
            request = f"""
                INSERT INTO 
                    permissions
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
                        {data.get("peer_id")},
                        {data.get("target_id")},
                        '{data.get("target_name")}',
                        '{data.get("target_url")}',
                        {data.get("target_set_role")},
                        '{data.get("target_set_role_name")}'
                    );
            """

        self.cursor.execute(request)
        self.connection.commit()

    def get_permission(self, peer_id, user_id) -> int:
        request = f"""
            SELECT 
                permission_lvl 
            FROM 
                permissions 
            WHERE 
                peer_id = {peer_id} 
            AND 
                user_id = {user_id};
        """
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return record[0][0]

        else:
            return 0

    """
     --------------------------------------------------------------------------------------------------------------------
    """

    def add_kick(self, data: Dict):
        request = f"""
            INSERT INTO 
                kicked 
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
                    {data.get("peer_id")}, 
                    {data.get("target_id")}, 
                    '{data.get("target_name")}', 
                    '{data.get("target_url")}', 
                    {data.get("initiator_id")}, 
                    '{data.get("initiator_name")}', 
                    '{data.get("initiator_url")}', 
                    {data.get("now_time_epoch")}
                );
        """
        self.cursor.execute(request)
        self.connection.commit()

    def get_kick(self, peer_id, user_id) -> List[int]:
        request = f"""
            SELECT 
                user_id 
            FROM 
                kicked 
            WHERE 
                peer_id = {peer_id} 
            AND 
                user_id = {user_id};
        """
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return [x[0] for x in record]

        else:
            return []

    """
     --------------------------------------------------------------------------------------------------------------------
    """

    def add_ban(self, data: Dict):
        request = f"""
            INSERT INTO 
                banned 
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
                    {data.get("peer_id")}, 
                    {data.get("target_id")}, 
                    '{data.get("target_name")}', 
                    '{data.get("target_url")}', 
                    {data.get("initiator_id")}, 
                    '{data.get("initiator_name")}', 
                    '{data.get("initiator_url")}', 
                    {data.get("now_time_epoch")},
                    {data.get("target_time_epoch")}
                );
        """
        self.cursor.execute(request)
        self.connection.commit()

    def remove_ban(self, peer_id, user_id):
        request = f"""
            DELETE FROM 
                banned 
            WHERE 
                peer_id = {peer_id} 
            AND 
                user_id = {user_id};
        """
        self.cursor.execute(request)
        self.connection.commit()

    def get_ban(self, peer_id, user_id) -> List[int]:
        request = f"""
            SELECT 
                user_id 
            FROM 
                banned 
            WHERE 
                peer_id = {peer_id} 
            AND 
                user_id = {user_id};
        """
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return [x[0] for x in record]

        else:
            return []

    def get_expired_ban(self, now_time):
        request = f"""
            SELECT 
                peer_id,
                user_id 
            FROM 
                banned
            WHERE 
                unban_time < {now_time} 
        """
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        return record

    """
     --------------------------------------------------------------------------------------------------------------------
    """

    def add_mute(self, data: Dict):
        request = f"""
            INSERT INTO 
                muted 
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
                    {data.get("peer_id")}, 
                    {data.get("target_id")}, 
                    '{data.get("target_name")}', 
                    '{data.get("target_url")}', 
                    {data.get("initiator_id")}, 
                    '{data.get("initiator_name")}', 
                    '{data.get("initiator_url")}', 
                    {data.get("now_time_epoch")},
                    {data.get("target_time_epoch")}
                );
        """
        self.cursor.execute(request)
        self.connection.commit()

    def remove_mute(self, peer_id, user_id):
        request = f"""
            DELETE FROM 
                muted 
            WHERE 
                peer_id = {peer_id} 
            AND 
                user_id = {user_id};
        """
        self.cursor.execute(request)
        self.connection.commit()

    def get_mute(self, peer_id, user_id) -> List[int]:
        request = f"""
            SELECT 
                user_id 
            FROM 
                muted 
            WHERE 
                peer_id = {peer_id} 
            AND 
                user_id = {user_id};
        """
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return [x[0] for x in record]

        else:
            return []

    def get_expired_mute(self, now_time):
        request = f"""
            SELECT 
                peer_id,
                user_id 
            FROM 
                muted 
            WHERE 
                unmute_time < {now_time} 
        """
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        return record

    """
     --------------------------------------------------------------------------------------------------------------------
    """

    def add_warn(self, data: Dict):
        request = f"""
                INSERT INTO 
                    warned 
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
                        {data.get("peer_id")}, 
                        {data.get("target_id")}, 
                        '{data.get("target_name")}', 
                        '{data.get("target_url")}', 
                        {data.get("initiator_id")}, 
                        '{data.get("initiator_name")}', 
                        '{data.get("initiator_url")}', 
                        {data.get("now_time_epoch")},
                        {data.get("target_time_epoch")},
                        {data.get("target_warns")}
                    );
            """
        self.cursor.execute(request)
        self.connection.commit()

    def remove_warn(self, peer_id, user_id, force=False):
        target_warns = self.get_warn(peer_id, user_id)

        if target_warns == 1 or force:
            request = f"""
                    DELETE FROM 
                        warned 
                    WHERE 
                        peer_id = {peer_id} 
                    AND 
                        user_id = {user_id};
                """

        else:
            request = f"""
                    UPDATE
                        warned
                    SET
                        warn_count = {target_warns - 1}
                    WHERE 
                        peer_id = {peer_id} 
                    AND 
                        user_id = {user_id};
                """
        self.cursor.execute(request)
        self.connection.commit()

    def get_warn(self, peer_id, user_id) -> int:
        request = f"""
                SELECT 
                    warn_count 
                FROM 
                    warned 
                WHERE 
                    peer_id = {peer_id} 
                AND 
                    user_id = {user_id};
            """
        self.cursor.execute(request)
        record = self.cursor.fetchone()

        if record:
            return record[0]

        return 0

    def get_expired_warn(self, now_time):
        request = f"""
            SELECT 
                peer_id,
                user_id 
            FROM 
                warned
            WHERE 
                unwarn_time < {now_time} 
        """
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        return record

    def get_overflow_warn(self):
        request = f"""
            SELECT 
                peer_id,
                user_id 
            FROM 
                warned
            WHERE 
                warn_count > 2
        """
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        return record

    """
    --------------------------------------------------------------------------------------------------------------------
    """

    def add_queue(self, data: Dict):
        request = f"""
                INSERT INTO 
                    queue
                    (
                        peer_id,
                        user_id,
                        user_name,
                        user_url,
                        send_time,
                        next_send_time
                    ) 
                VALUES
                    (
                        {data.get("peer_id")}, 
                        {data.get("initiator_id")}, 
                        '{data.get("initiator_name")}', 
                        '{data.get("initiator_url")}', 
                        {data.get("now_time_epoch")},
                        {data.get("target_time_epoch")}
                    );
            """

        self.cursor.execute(request)
        self.connection.commit()

    def remove_queue(self, peer_id, user_id):
        request = f"""
            DELETE FROM 
                queue
            WHERE 
                peer_id = {peer_id} 
            AND 
                user_id = {user_id};
        """
        self.cursor.execute(request)
        self.connection.commit()

    def get_queue(self, peer_id, user_id):
        request = f"""
                SELECT 
                    peer_id,
                    user_id
                FROM 
                    queue
                WHERE 
                    peer_id = {peer_id}
                AND 
                    user_id = {user_id};
            """
        self.cursor.execute(request)
        record = self.cursor.fetchone()

        if record:
            return record[0]

        return ()

    def get_expired_queue(self, now_time):
        request = f"""
                SELECT 
                    peer_id,
                    user_id
                FROM 
                    queue
                WHERE 
                    next_send_time < {now_time};
            """
        self.cursor.execute(request)
        record = self.cursor.fetchone()

        if record:
            return record[0]

        return ()

    """
    --------------------------------------------------------------------------------------------------------------------
    """


if __name__ == "__main__":
    database = Connection('database.db')
    print(database.version())
    database.debug()
    print(database.get_setting(peer_id=2000000002, setting_name="Allow_Picture"))
