from routes.filters.core import *
from vkbottle.bot import Message, BotLabeler
from routes.rules import IgnorePermission, HandleIn, OnlyEnrolled


bl = BotLabeler()


@bl.chat_message(
    IgnorePermission(ignore_from=1, mode="SELF"),
    HandleIn(handle_log=False, handle_chat=True, send_respond=False),
    OnlyEnrolled(send_respond=False),
    blocking=False
)
async def pm_filter(message: Message):
    ...