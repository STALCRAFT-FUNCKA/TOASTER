import sqlite3
from DataBase import tables

class Connection:

    def _fill_std_form(self):
        for table in tables:
            self.cursor.execute(table)

    def __init__(self, filename: str):
        self.db = filename

        try:
            self.connection = sqlite3.connect(self.db)
            self.cursor = self.connection.cursor()
            print("База данных создана и успешно подключена к SQLite")

            self._fill_std_form()

        except sqlite3.Error as error:
            print("Ошибка при подключении к SQLite", error)

    def version(self):
        self.cursor.execute("select sqlite_version();")
        record = self.cursor.fetchall()
        return record

    def get_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.cursor.execute("SELECT PeerID, PeerName FROM conversation;")
        record = self.cursor.fetchall()

        return record

    def add_conversation(self, PeerID:int, PeerName:str):
        request = f"""INSERT INTO conversation (PeerID, PeerName) 
                        VALUES ({PeerID}, '{PeerName}');"""
        self.cursor.execute(request)
        self.connection.commit()

    def remove_conversation(self, PeerID:int):
        request = f"""DELETE FROM conversation WHERE PeerID = {PeerID};"""
        self.cursor.execute(request)
        self.connection.commit()

    def add_kick(self, PeerID:int, UserID:int, UserName:str, UserURL:str,
                 KickedByID:int, KickedByName:str, KickedByURL:str, KickTime:int):
        request = f"""INSERT INTO kicked (PeerID, UserID, UserName, UserURL, 
                                            KickedByID, KickedByName, KickedByURL, KickTime) 
                    VALUES ({PeerID}, {UserID}, '{UserName}', '{UserURL}', 
                            {KickedByID}, '{KickedByName}', '{KickedByURL}', {KickTime});"""
        self.cursor.execute(request)
        self.connection.commit()


    def add_ban(self, PeerID:int, UserID:int, UserName:str, UserURL:str,
                 BannedByID:int, BannedByName:str, BannedByURL:str, BanTime:int, UnbanTime:int):
        request = f"""INSERT INTO banned (PeerID, UserID, UserName, UserURL, 
                                            BannedByID, BannedByName, BannedByURL, BanTime, UnbanTime) 
                            VALUES ({PeerID}, {UserID}, '{UserName}', '{UserURL}', 
                                    {BannedByID}, '{BannedByName}', '{BannedByURL}', {BanTime}, {UnbanTime});"""
        self.cursor.execute(request)
        self.connection.commit()

    def remove_ban(self, PeerID:int, UserID:int):
        request = f"""DELETE FROM banned WHERE PeerID = {PeerID} AND UserID = {UserID};"""
        self.cursor.execute(request)
        self.connection.commit()

    def add_mute(self, PeerID:int, UserID:int, UserName:str, UserURL:str,
                 MutedByID:int, MutedByName:str, MutedByURL:str, MuteTime:int, UnmuteTime:int):
        request = f"""INSERT INTO muted (PeerID, UserID, UserName, UserURL, 
                                                    BannedByID, BannedByName, BannedByURL, BanTime, UnbanTime) 
                                    VALUES ({PeerID}, {UserID}, '{UserName}', '{UserURL}', 
                                            {MutedByID}, '{MutedByName}', '{MutedByURL}', {MuteTime}, {UnmuteTime});"""
        self.cursor.execute(request)
        self.connection.commit()


    def remove_mute(self, PeerID:int, UserID:int):
        request = f"""DELETE FROM muted WHERE PeerID = {PeerID} AND UserID = {UserID};"""
        self.cursor.execute(request)
        self.connection.commit()

    def add_warn(self, PeerID:int, UserID:int, UserName:str, UserURL:str,
                 WarnedByID:int,  WarnedByName:str,  WarnedByURL:str,  WarnTime:int, UnwarnTime:int, WarnCount:int):
        request = f"""INSERT INTO muted (PeerID, UserID, UserName, UserURL, 
                                                    BannedByID, BannedByName, BannedByURL, BanTime, UnbanTime) 
                                    VALUES ({PeerID}, {UserID}, '{UserName}', '{UserURL}', 
                                            {WarnedByID}, '{WarnedByName}', '{WarnedByURL}', {WarnTime}, {UnwarnTime});"""
        self.cursor.execute(request)
        self.connection.commit()
        # TODO: Make warn-count checking

    def remove_warn(self, PeerID:int, UserID:int):
        request = f"""DELETE FROM warned WHERE PeerID = {PeerID} AND UserID = {UserID};"""
        self.cursor.execute(request)
        self.connection.commit()
        # TODO: Make warn-count checking




if __name__ == "__main__":
    database = Connection('database.db')
    print(database.version())
    print(database.get_tables())
