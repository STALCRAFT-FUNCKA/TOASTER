import sqlite3

from DataBase import tables

class Tools:

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

    def add_kick(self, PeerID:int,UserID:int, UserName:str, UserURL:str,
                 KickedByID:int, KickedByName:str, KickedByURL:str, KickTime:int):
        request = f"""INSERT INTO kicked (PeerID, UserID, UserName, UserURL, 
                                            KickedByID, KickedByName, KickedByURL, KickTime) 
                    VALUES ({PeerID}, {UserID}, '{UserName}', '{UserURL}', 
                            {KickedByID}, '{KickedByName}', '{KickedByURL}', {KickTime});"""
        self.cursor.execute(request)
        self.connection.commit()

    def remove_kick(self):
        pass

    def add_ban(self):
        pass

    def remove_ban(self):
        pass

    def add_mute(self):
        pass

    def remove_mute(self):
        pass

    def add_warn(self):
        pass

    def remove_warn(self):
        pass




if __name__ == "__main__":
    database = Tools('database.db')
    database.add_conversation(PeerID=2124124, PeerName='SUKA')
    print(database.version())
    print(database.get_tables())
    database.remove_conversation(PeerID=2124124)
