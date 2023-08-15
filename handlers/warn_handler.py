import time
from .abc_handler import ABCHandler


class Handler(ABCHandler):
    async def check(self):
        expired = self.database.get_expired_warn(time.time())
        if expired:
            for warn in expired:
                self.database.remove_warn(peer_id=warn[0], user_id=warn[1], force=True)
                await self._send_log(peer_id=warn[0], user_id=warn[1], command="unwarn")
