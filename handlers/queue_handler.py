import time
from .abc_handler import ABCHandler


class Handler(ABCHandler):
    async def check(self):
        expired = self.database.get_expired_queue(time.time())
        if expired:
            for q in expired:
                self.database.remove_queue(peer_id=q[0], user_id=q[1])