from typing import Optional
from DataBase.Utils import Connection

database = Connection('DataBase/database.db')

class Logger:

    @staticmethod
    def _get_log_peers():
        return [x[0] for x in database.get_conversation(PeerID=-1, Destination="LOG")]

    def send_log(self, log: Optional[dict] = None):
        peers = self._get_log_peers()

        for PeerID in peers:
            ...