from vkbottle.bot import BotLabeler, Message
from config import GROUP_ID, GROUP_URL, CURSE_WORDS
from database import Processor
from routes.rules import IgnorePermission, HandleIn, OnlyEnrolled
from utils import *


bl = BotLabeler()

info = Info()
converter = Converter()
processor = Processor()


@bl.chat_message(
    IgnorePermission(ignore_from=1, mode="SELF"),
    HandleIn(handle_log=False, handle_chat=True, send_respond=False),
    OnlyEnrolled(send_respond=False),
    blocking=False
)
async def curse_filter(message: Message):
    check = processor.subproc.setting_get_sub(
        peer_id=message.peer_id,
        setting_name="Age_Check"
    )
    if not check:
        return

    for word in CURSE_WORDS:
        if word in message.text:
            reason = "Нежелательное слово"
            context = {
                "peer_id": message.peer_id,
                "peer_name": await info.peer_name(message.peer_id),
                "chat_id": message.chat_id,
                "initiator_id": 0,
                "initiator_name": "Система",
                "initiator_nametag": "Система",
                "command_name": "delete",
                "reason": reason,
                "now_time": converter.now(),
                "cmids": [message.conversation_message_id],
            }

            await processor.delete_proc(context, log=True, respond=False)
