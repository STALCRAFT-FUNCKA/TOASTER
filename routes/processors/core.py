"""
File with description of abstract processor.
"""

from vkbottle import Bot
from config import (
    TOKEN,
)
from utils import Converter, Informer
from data import DataBase
from .logger import Logger


class StdProcessor:
    """
    Template of processor class which contains all the dependencies necessary.
    """

    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.database = DataBase()
        self.logger = Logger()
        self.info = Informer()
        self.converter = Converter()

    async def _send_respond(self, text, ctx):
        await self.bot.api.messages.send(
            chat_id=ctx.get("chat_id"),
            message=text,
            random_id=0
        )

    async def _send_log(self, ctx):
        self.logger.compose_log_data(ctx)
        self.logger.compose_log_attachments(ctx)
        await self.logger.log()

    def _get_initiator_lvl(self, context):
        role = self.database.permissions.select(
            ("target_lvl",),
            peer_id=context.get("peer_id"),
            target_id=context.get("initiator_id")
        )
        if role:
            return role[0][0]

        return 0
