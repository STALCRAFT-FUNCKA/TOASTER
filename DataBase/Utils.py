import sqlite3
from typing import List

from DataBase import tables

class Connection:

    def _fill_std_form(self):
        for table in tables:
            self.cursor.execute(table)

    """
    --------------------------------------------------------------------------------------------------------------------
    """
    def __init__(self, filename: str, allow_debug_text: bool = False):
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
        self.cursor.execute("SELECT PeerID, PeerName FROM conversation;")
        record = self.cursor.fetchall()
        print('Беседы:', record)
        self.cursor.execute("SELECT SettingName, SettingStatus FROM setting WHERE PeerID = 2000000002;")
        record = self.cursor.fetchall()
        print('Настройки:', record)

    """
    --------------------------------------------------------------------------------------------------------------------
    """
    def add_conversation(self, PeerID:int, PeerName:str, Destination:str):
        request = f"""INSERT INTO conversation 
                        (
                            PeerID, 
                            PeerName,
                            Destination
                        ) 
                        VALUES 
                        (
                            {PeerID}, 
                            '{PeerName}',
                            '{Destination}'
                        );"""
        self.cursor.execute(request)
        self.connection.commit()

    def remove_conversation(self, PeerID:int):
        request = f"""DELETE FROM conversation WHERE PeerID = {PeerID};"""
        self.cursor.execute(request)
        self.connection.commit()

    def get_conversation(self, PeerID:int, Destination:str) -> List[int]:
        if PeerID == -1:
            request = f"""SELECT PeerID conversation WHERE Destination = '{Destination}'"""
        else:
            request = f"""SELECT PeerID FROM conversation WHERE PeerID = {PeerID} AND Destination = '{Destination}'"""

        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return [x[0] for x in record]
        else:
            return []

    """
    --------------------------------------------------------------------------------------------------------------------
    """
    def add_setting(self,SettingName:str, SettingStatus:bool, PeerID:int):
        request = f"""INSERT INTO setting 
                        (
                            SettingName, 
                            SettingStatus, 
                            PeerID
                        ) 
                        VALUES 
                        (   
                            '{SettingName}', 
                            '{SettingStatus}', 
                            {PeerID}
                        );"""
        self.cursor.execute(request)
        self.connection.commit()

    def get_setting(self,SettingName:str, PeerID:int) -> bool:
        request = f"""SELECT SettingStatus FROM setting WHERE SettingName = '{SettingName}' AND PeerID = {PeerID}"""
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return record[0][0]

    """
     --------------------------------------------------------------------------------------------------------------------
    """
    def set_permission(self, UserID:int, UserName:str, UserURL:str, PermissionLvl:int, PermissionName:str, PeerID:int):
        request = ""
        if PermissionLvl < 1:
            request = f"""DELETE FROM permission WHERE UserID = {UserID} AND PeerID = {PeerID};"""

        elif PermissionLvl < 3:
            request = f"""INSERT INTO permission 
                        (
                           UserID,
                           UserName,
                           UserURL,
                           PermissionLvl,
                           PermissionName,
                           PeerID
                        )
                        VALUES 
                        (
                           {UserID},
                           '{UserName}',
                           '{UserURL}',
                           {PermissionLvl},
                           '{PermissionName}',
                           {PeerID}
                        );"""

        self.cursor.execute(request)
        self.connection.commit()

    def get_permission(self, PeerID:int, UserID:int) -> int:
        request = f"""SELECT PermissionLvl FROM permission WHERE PeerID = {PeerID} AND UserID = {UserID};"""
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return  record[0][0]

        else:
            return 0

    """
     --------------------------------------------------------------------------------------------------------------------
    """
    def add_kick(self, PeerID:int, UserID:int, UserName:str, UserURL:str,
                 KickedByID:int, KickedByName:str, KickedByURL:str, KickTime:int):
        request = f"""INSERT INTO kicked 
                        (
                            PeerID,
                            UserID, 
                            UserName, 
                            UserURL, 
                            KickedByID, 
                            KickedByName, 
                            KickedByURL, 
                            KickTime
                        ) 
                        VALUES 
                        (
                            {PeerID}, 
                            {UserID}, 
                            '{UserName}', 
                            '{UserURL}', 
                            {KickedByID}, 
                            '{KickedByName}', 
                            '{KickedByURL}', 
                            {KickTime}
                        );"""
        self.cursor.execute(request)
        self.connection.commit()

    def get_kick(self, PeerID:int, UserID:int) -> List[int]:
        request = f"""SELECT UserID FROM kicked WHERE PeerID = {PeerID} AND UserID = {UserID};"""
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return [x[0] for x in record]

        else:
            return []
    """
     --------------------------------------------------------------------------------------------------------------------
    """
    def add_ban(self, PeerID:int, UserID:int, UserName:str, UserURL:str,
                 BannedByID:int, BannedByName:str, BannedByURL:str, BanTime:int, UnbanTime:int):
        request = f"""INSERT INTO banned 
                        (
                            PeerID, 
                            UserID, 
                            UserName, 
                            UserURL, 
                            BannedByID, 
                            BannedByName, 
                            BannedByURL, 
                            BanTime, 
                            UnbanTime
                        ) 
                        VALUES 
                        (
                            {PeerID}, 
                            {UserID}, 
                            '{UserName}', 
                            '{UserURL}', 
                            {BannedByID}, 
                            '{BannedByName}', 
                            '{BannedByURL}', 
                            {BanTime},
                            {UnbanTime}
                        );"""
        self.cursor.execute(request)
        self.connection.commit()

    def remove_ban(self, PeerID:int, UserID:int):
        request = f"""DELETE FROM banned WHERE PeerID = {PeerID} AND UserID = {UserID};"""
        self.cursor.execute(request)
        self.connection.commit()

    def get_ban(self, PeerID: int, UserID: int) -> List[int]:
        request = f"""SELECT UserID FROM banned WHERE PeerID = {PeerID} AND UserID = {UserID};"""
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return [x[0] for x in record]

        else:
            return []

    """
     --------------------------------------------------------------------------------------------------------------------
    """
    def add_mute(self, PeerID:int, UserID:int, UserName:str, UserURL:str,
                 MutedByID:int, MutedByName:str, MutedByURL:str, MuteTime:int, UnmuteTime:int):
        request = f"""INSERT INTO muted 
                        (
                            PeerID, 
                            UserID, 
                            UserName, 
                            UserURL, 
                            BannedByID, 
                            BannedByName, 
                            BannedByURL, 
                            BanTime, 
                            UnbanTime
                        ) 
                        VALUES 
                        (
                            {PeerID}, 
                            {UserID}, 
                            '{UserName}', 
                            '{UserURL}', 
                            {MutedByID}, 
                            '{MutedByName}', 
                            '{MutedByURL}', 
                            {MuteTime}, 
                            {UnmuteTime}
                        );"""
        self.cursor.execute(request)
        self.connection.commit()


    def remove_mute(self, PeerID:int, UserID:int):
        request = f"""DELETE FROM muted WHERE PeerID = {PeerID} AND UserID = {UserID};"""
        self.cursor.execute(request)
        self.connection.commit()

    def get_mute(self, PeerID: int, UserID: int) -> List[int]:
        request = f"""SELECT UserID FROM muted WHERE PeerID = {PeerID} AND UserID = {UserID};"""
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return [x[0] for x in record]

        else:
            return []
    """
     --------------------------------------------------------------------------------------------------------------------
    """
    def add_warn(self, PeerID:int, UserID:int, UserName:str, UserURL:str,
                 WarnedByID:int,  WarnedByName:str,  WarnedByURL:str,  WarnTime:int, UnwarnTime:int, WarnCount:int):
        request = f"""INSERT INTO muted (PeerID, UserID, UserName, UserURL, 
                                                    BannedByID, BannedByName, BannedByURL, BanTime, UnbanTime) 
                                    VALUES ({PeerID}, {UserID}, '{UserName}', '{UserURL}', 
                                            {WarnedByID}, '{WarnedByName}', '{WarnedByURL}', {WarnTime}, {UnwarnTime});"""
        self.cursor.execute(request)
        self.connection.commit()
        # TODO: Сдилать првоерку на кол-во варнов

    def remove_warn(self, PeerID:int, UserID:int):
        request = f"""DELETE FROM warned WHERE PeerID = {PeerID} AND UserID = {UserID};"""
        self.cursor.execute(request)
        self.connection.commit()
        # TODO: Сделать проверку на кол-во варнов

    def get_warn(self, PeerID: int, UserID: int) -> int:
        request = f"""SELECT WarnCount FROM warned WHERE PeerID = {PeerID} AND UserID = {UserID};"""
        self.cursor.execute(request)
        record = self.cursor.fetchall()
        if record:
            return record[0][0]

        else:
            return 0

    """
     --------------------------------------------------------------------------------------------------------------------
    """



if __name__ == "__main__":
    database = Connection('database.db')
    print(database.version())
    database.debug()
    print(database.get_setting(PeerID=2000000002, SettingName="Allow_Picture"))
