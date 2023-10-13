"""
This file describes the inherited class queue handler.
"""

from routes.handlers.core import BaseHandler


class Handler(BaseHandler):
    """
    Checks the database for expired messages in queue. Removes them, if any.
    """

    async def check(self):
        expired = self.database.queue.select(
            ("peer_id", "target_id"),
            next_time__le=self.converter.now()
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
                    "command_name": "unqueue",
                    "now_time": self.converter.now(),
                }

                await self.processor.unqueue_proc(context, log=False, respond=False)

    def egg(self):
        """
        Thanks you SindeyJob! :)
        """
        return
