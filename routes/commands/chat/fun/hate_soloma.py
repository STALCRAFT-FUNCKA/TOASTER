from routes.commands.core import *
from config import PERMISSION_ACCESS, ALIASES, PREFIXES
from vkbottle.bot import Message, BotLabeler
from typing import Tuple
from routes.rules import *

bl = BotLabeler()


@bl.chat_message(
    HandleCommand(ALIASES['hate_soloma'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['hate_soloma']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def hate_soloma(message: Message, args: Tuple):
    context = {
        "peer_id": message.peer_id,
        "peer_name": await informer.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await informer.user_name(message.from_id, tag=False),
        "initiator_nametag": await informer.user_name(message.from_id, tag=True),
        "command_name": "hate_soloma",
        "now_time": converter.now(),
    }

# Сделать чото
