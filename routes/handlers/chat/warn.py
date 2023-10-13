"""
This file describes the inherited class expired warns handler.
"""

from routes.handlers.core import ABCHandler
from data import DataBase


class Handler(ABCHandler):
    """
    Checks the database for expired warns in queue. Removes them, if any.
    """

    database = DataBase()
    
    async def check(self):
        expired = self.database.warned.select(
            ("peer_id", "target_id"),
            unwarn_time__le=self.converter.now()
        )
        if expired:
            for peer_id, target_id in expired:
                context = {
                    "peer_id": peer_id,
                    "peer_name": await self.informer.peer_name(peer_id),
                    "chat_id": peer_id - 2000000000,
                    "initiator_id": 0,
                    "initiator_name": "Система",
                    "initiator_nametag": "Система",
                    "target_id": target_id,
                    "target_name": await self.informer.user_name(
                        target_id, tag=False
                    ),
                    "target_nametag": await self.informer.user_name(
                        target_id, tag=True
                    ),
                    "command_name": "unwarn",
                    "now_time": self.converter.now(),
                }

                await self. processor.unwarn_proc(context, force=True)

    def egg(self):
        """
        hehe-he :)
        """
        return
    