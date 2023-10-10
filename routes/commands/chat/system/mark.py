"""
File with /mark bot command.
"""

from typing import Tuple
from vkbottle.bot import (
    Message,
    BotLabeler
)
from routes.commands.core import (
    informer,
    converter,
    com_processor
)
from routes.rules import (
    HandleCommand,
    CollapseCommand,
    AllowAnswer,
    CheckPermission,
    HandleIn
)
from config import (
    PERMISSION_ACCESS,
    ALIASES,
    PREFIXES
)



bl = BotLabeler()


@bl.chat_message(
    HandleCommand(ALIASES['mark'], PREFIXES, 1),
    CollapseCommand(),
    AllowAnswer(allow_reply=False, allow_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['mark']),
    HandleIn(handle_log=True, handle_chat=True)
)
async def mark(message: Message, args: Tuple):
    """
    This function describes the logic behind the /mark command.
    
    Args:
        message (Message): vkbottle message object.
        args (Tuple): tuple of command arguments.
    """

    context = {
        "peer_id": message.peer_id,
        "peer_name": await informer.peer_name(message.peer_id),
        "peer_type": None,
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await informer.user_name(message.from_id, tag=False),
        "initiator_nametag": await informer.user_name(message.from_id, tag=True),
        "command_name": None,
        "now_time": converter.now(),
    }

    if args[0] == "chat":
        context["peer_type"] = "CHAT"
        context["command_name"] = "mark chat"
        await com_processor.chat_proc(context)

    if args[0] == "log":
        context["peer_type"] = "LOG"
        context["command_name"] = "mark log"
        await com_processor.log_proc(context)

    if args[0] == "drop":
        context["command_name"] = "mark drop"
        await com_processor.drop_proc(context)
