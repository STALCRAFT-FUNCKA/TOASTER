from config import ALIASES, PREFIXES, PERMISSION_LVL, PERMISSION_ACCESS, QUEUE_TIME
from vkbottle.bot import BotLabeler, Message
from database.proc import Processor
from typing import Tuple
from utils import *
from .rules import *


bl = BotLabeler()

info = Info()
converter = Converter()
processor = Processor()


@bl.chat_message(
    HandleCommand(ALIASES['info'], PREFIXES, 1),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['info']),
    HandleIn(handle_log=True, handle_chat=False)
)
async def info(message: Message, args: Tuple):
    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "command_name": "info" + args[0],
        "now_time": converter.now()
    }

    await processor.reference_proc(context, log=False, respond=True)