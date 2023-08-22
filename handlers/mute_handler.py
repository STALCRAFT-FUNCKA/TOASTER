import time
from additionals.ABCHandler import ABCHandler


class Handler(ABCHandler):
    async def check(self):
        expired = self.database.get_expired_mute(time.time())
        if expired:
            for mute in expired:
                self.database.remove_mute(peer_id=mute[0], user_id=mute[1])
                await self._send_log(peer_id=mute[0], user_id=mute[1], command="unmute")
