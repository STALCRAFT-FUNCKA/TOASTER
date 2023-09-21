import random
from routes.commands.core import *
from config import PERMISSION_ACCESS, ALIASES, PREFIXES
from vkbottle.bot import Message, BotLabeler
from typing import Tuple
from routes.rules import *


bl = BotLabeler()


@bl.chat_message(
    HandleCommand(ALIASES['say'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['say']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def say(message: Message, args: Tuple):
    context = {
        "peer_id": message.peer_id,
        "peer_name": await informer.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await informer.user_name(message.from_id, tag=False),
        "initiator_nametag": await informer.user_name(message.from_id, tag=True),
        "command_name": "say",
        "now_time": converter.now(),
        "say_text": None
    }

    if not args:
        return

    say_text = " ".join(args)
    context["say_text"] = say_text

    await fun_processor.fun_say_proc(context, log=True, respond=False)