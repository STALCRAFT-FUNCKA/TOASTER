"""
File with /permission bot command.
"""

from typing import Tuple
from vkbottle.bot import (
    Message,
    BotLabeler
)
from routes.rules import (
    HandleIn,
    HandleCommand,
    CheckPermission,
    OnlyEnrolled,
    CollapseCommand
)
from routes.commands.core import (
    informer,
    com_processor,
    converter,
    get_cuid
)
from config import (
    PERMISSION_ACCESS,
    PERMISSION_LVL,
    ALIASES,
    PREFIXES
)


bl = BotLabeler()


@bl.chat_message(
    HandleCommand(ALIASES['permission'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['permission']),
    HandleIn(handle_log=True, handle_chat=True),
    OnlyEnrolled()
)
async def permission(message: Message, args: Tuple):
    """
    This function describes the logic behind the /permission command.
    
    Args:
        message (Message): vkbottle message object.
        args (Tuple): tuple of command arguments.
    """

    if not args or message.fwd_messages:
        return

    try:
        lvl = int(args[0])
        if lvl not in PERMISSION_LVL:
            lvl = 0
    except TypeError:
        lvl = 0

    context = {
        "peer_id": message.peer_id,
        "peer_name": await informer.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await informer.user_name(message.from_id, tag=False),
        "initiator_nametag": await informer.user_name(message.from_id, tag=True),
        "target_id": None,
        "target_name": None,
        "target_nametag": None,
        "target_lvl": lvl,
        "command_name": "permission",
        "now_time": converter.now(),
    }

    if len(args) == 1 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await informer.user_name(
            message.reply_message.from_id, tag=False
        )
        context["target_nametag"] = await informer.user_name(
            message.reply_message.from_id, tag=True
        )

    elif len(args) == 2 and not message.reply_message:
        cuid = await get_cuid(args[1])
        if cuid is None:
            print("Command aborted: Wrong mention")
            return

        context["target_id"] = cuid
        context["target_name"] = await informer.user_name(cuid, tag=False)
        context["target_nametag"] = await informer.user_name(cuid, tag=True)

    else:
        return

    await com_processor.permission_proc(context, respond=False)
