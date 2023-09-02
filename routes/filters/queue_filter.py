from vkbottle.bot import BotLabeler, Message

from database.orm import DataBase
from database.proc import Processor
from routes.rules import IgnorePermission, HandleIn, OnlyEnrolled
from utils import *


bl = BotLabeler()

info = Info()
converter = Converter()
database = DataBase()
processor = Processor()


@bl.chat_message(
    IgnorePermission(ignore_from=1, mode="SELF"),
    HandleIn(handle_log=False, handle_chat=True, send_respond=False),
    OnlyEnrolled(send_respond=False),
    blocking=False
)
async def queue(message: Message):
    is_muted = database.muted.select(
        ("target_name",),
        peer_id=message.peer_id,
        target_id=message.from_id
    )
    if is_muted:
        return

    check = database.settings.select(
        ("setting_status",),
        peer_id=message.peer_id,
        setting_name='Slow_Mode'
    )
    check = check[0][0] if check else False
    check = True if check == "True" else False
    if not check:
        return

    reason = "Нарушение задержки"
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
        "command_name": "warn",
        "reason": reason,
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficent),
        "cmids": [message.conversation_message_id]
    }

    in_queue = database.queue.select(
        ("target_name",),
        peer_id=message.peer_id,
        target_id=message.from_id
    )
    if in_queue:
        await processor.warn_proc(context, collapse=True, log=True, respond=True)
    else:
        await processor.queue_proc(context, log=False, respond=False)
