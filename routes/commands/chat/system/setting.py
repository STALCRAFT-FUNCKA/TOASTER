"""
File with /setting bot command.
"""

from typing import Tuple
from vkbottle.bot import (
    Message,
    BotLabeler
)
from routes.commands.core import (
    informer,
    com_processor,
    converter
)
from routes.rules import (
    HandleCommand,
    CollapseCommand,
    AllowAnswer,
    CheckPermission,
    HandleIn,
    OnlyEnrolled
)
from config import (
    PERMISSION_ACCESS,
    ALIASES,
    PREFIXES
)


bl = BotLabeler()


@bl.chat_message(
    HandleCommand(ALIASES['setting'], PREFIXES, 2),
    CollapseCommand(),
    AllowAnswer(allow_reply=False, allow_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['setting']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def setting(message: Message, args: Tuple):
    """
    This function describes the logic behind the /setting command.
    
    Args:
        message (Message): vkbottle message object.
        args (Tuple): tuple of command arguments.
    """
    
    setting_name = args[0]
    try:
        setting_status = int(args[1])
    except TypeError:
        setting_status = 0

    context = {
        "peer_id": message.peer_id,
        "peer_name": await informer.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await informer.user_name(message.from_id, tag=False),
        "initiator_nametag": await informer.user_name(message.from_id, tag=True),
        "command_name": "setting",
        "setting_name": setting_name,
        "setting_status": 1 if setting_status else 0,
        "now_time": converter.now()
    }

    await com_processor.setting_proc(context, respond=False)
