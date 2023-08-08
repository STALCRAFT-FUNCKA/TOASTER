import json
from typing import Dict

from Config import GROUP, TOKEN
from DataBase.Interface import Connection

from vkbottle.bot import Bot

database = Connection('DataBase/database.db')

class Logger:
    def __init__ (self):
        self.bot = Bot(token = TOKEN)

    @staticmethod
    def _get_log_peers():
        return database.get_conversation(PeerID=-1, Destination="LOG")

    async def send_log(self, log):
        peers = self._get_log_peers()

        for PeerID in peers:
            await self.bot.api.messages.send(
                group_id=GROUP,
                peer_id=PeerID,
                message=log['text'],
                forward=json.dumps(log['forward']),
                random_id=0
            )