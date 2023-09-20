from ..core import ABCHandler


class Handler(ABCHandler):
    async def check(self):
        overflow = self.database.warned.select(
            ("peer_id", "target_id"),
            warn_count__ge=3
        )
        if overflow:
            for peer_id, target_id in overflow:
                time = 1
                coefficient = "d"

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
                    "command_name": "mute",
                    "now_time": self.converter.now(),
                    "target_time": self.converter.now() + self.converter.delta(time, coefficient),
                }

                await self.processor.mute_proc(context, log=True, respond=True)
                await self.processor.unwarn_proc(context, force=True, log=False, respond=False)
