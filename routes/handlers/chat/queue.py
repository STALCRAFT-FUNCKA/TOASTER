from routes.handlers.core import ABCHandler


class Handler(ABCHandler):
    async def check(self):
        expired = self.database.queue.select(
            ("peer_id", "target_id"),
            next_time__le=self.converter.now()
        )
        self.debug(f"expired: {expired}")
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
                    "target_name": await self.informer.user_name(target_id, tag=False),
                    "target_nametag": await self.informer.user_name(target_id, tag=True),
                    "command_name": "unqueue",
                    "now_time": self.converter.now(),
                }

                self.debug(f"making unqueue proc")
                
                await self.processor.unqueue_proc(context, log=False, respond=True)
