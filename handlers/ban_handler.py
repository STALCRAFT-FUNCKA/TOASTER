import time
from .abc_handler import ABCHandler


class Handler(ABCHandler):
    async def check(self):
        expired = self.database.get_expired_ban(time.time())
        if expired:
            for ban in expired:
                self.database.remove_ban(peer_id=ban[0], user_id=ban[1])
                await self._send_log(peer_id=ban[0], user_id=ban[1], command="unban")
