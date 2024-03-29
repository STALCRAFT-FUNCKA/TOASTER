"""
File with /info bot command.
"""

from typing import Tuple
from vkbottle.bot import (
    Message,
    BotLabeler
)
from routes.commands.core import (
    info_processor
)
from routes.rules import (
    HandleCommand,
    CollapseCommand,
    CheckPermission,
    HandleIn,
    AllowAnswer,
)
from config import (
    PERMISSION_ACCESS,
    ALIASES,
    PREFIXES
)

bl = BotLabeler()


@bl.chat_message(
    HandleCommand(ALIASES['info'], PREFIXES, 1),
    CollapseCommand(),
    AllowAnswer(allow_reply=False, allow_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['info']),
    HandleIn(handle_log=True, handle_chat=False)
)
async def info(message: Message, args: Tuple):
    """
    This function describes the logic behind the /info command.
    
    Args:
        message (Message): vkbottle message object.
        args (Tuple): tuple of command arguments.
    """

    context = {
        "peer_id": message.peer_id,
        "chat_id": message.chat_id
    }

    args_check = [
        (ALIASES['permission'], info_processor.info_permission_proc),
        (ALIASES['setting'], info_processor.info_setting_proc),
        (ALIASES['mark'], info_processor.info_mark_proc),
        (ALIASES['kick'], info_processor.info_kick_proc),
        (ALIASES['ban'], info_processor.info_ban_proc),
        (ALIASES['mute'], info_processor.info_mute_proc),
        (ALIASES['warn'], info_processor.info_warn_proc),
    ]

    for name, proc in args_check:
        if args[0] in name:
            await proc(context)
