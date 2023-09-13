from vkbottle.bot import BotLabeler, Message
from database.orm import DataBase
from database.proc import CommandProcessor
from routes.rules import IgnorePermission, HandleIn, OnlyEnrolled
from utils import *

bl = BotLabeler()

info = Info()
database = DataBase()
converter = Converter()
processor = CommandProcessor()


@bl.chat_message(
    IgnorePermission(ignore_from=1, mode="SELF"),
    HandleIn(handle_log=False, handle_chat=True, send_respond=False),
    OnlyEnrolled(send_respond=False),
    blocking=False
)
async def mute_filter(message: Message):
    is_muted = database.muted.select(
        ("target_name",),
        peer_id=message.peer_id,
        target_id=message.from_id
    )
    if not is_muted:
        return

    time = 1
    coefficent = "d"

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": 0,
        "initiator_name": "Система",
        "initiator_nametag": "Система",
        "target_id": message.from_id,
        "target_name": await info.user_name(message.from_id, tag=False),
        "target_nametag": await info.user_name(message.from_id, tag=True),
        "command_name": "ban",
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficent),
        "cmids": [message.conversation_message_id]
    }

    await processor.unmute_proc(context, log=False, respond=False)
    await processor.ban_proc(context, collapse=True, log=True, respond=True)
