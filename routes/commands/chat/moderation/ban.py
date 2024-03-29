"""
File with /ban and /unban bot commands.
"""

from typing import Tuple
from vkbottle.bot import (
    Message,
    BotLabeler
)
from routes.commands.core import (
    informer,
    converter,
    com_processor,
    get_cuid
)
from routes.rules import (
    HandleCommand,
    CollapseCommand,
    CheckPermission,
    HandleIn,
    IgnorePermission,
    OnlyEnrolled
)
from config import (
    PERMISSION_ACCESS,
    ALIASES,
    PREFIXES
)

bl = BotLabeler()


@bl.chat_message(
    HandleCommand(ALIASES['ban'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['ban']),
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def ban(message: Message, args: Tuple):
    """
    This function describes the logic behind the /ban command.
    
    Args:
        message (Message): vkbottle message object.
        args (Tuple): tuple of command arguments.
    """

    if not args or message.fwd_messages:
        return

    try:
        time = int(args[0])
        coefficient = args[1]
    except ValueError:
        time = 1
        coefficient = "h"

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
        "command_name": "ban",
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficient),
        "cmids": None
    }

    collapse = False

    if len(args) == 2 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await informer.user_name(
            message.reply_message.from_id, tag=False
        )
        context["target_nametag"] = await informer.user_name(
            message.reply_message.from_id, tag=True
        )
        context["cmids"] = [message.reply_message.conversation_message_id]
        collapse = True

    elif len(args) == 3 and not message.reply_message:
        cuid = await get_cuid(args[2])
        if cuid is None:
            print("Command aborted: Wrong mention")
            return

        context["target_id"] = cuid
        context["target_name"] = await informer.user_name(cuid, tag=False)
        context["target_nametag"] = await informer.user_name(cuid, tag=True)

    else:
        return

    await com_processor.ban_proc(context, collapse=collapse)


@bl.chat_message(
    HandleCommand(ALIASES['unban'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['unban']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unban(message: Message, args: Tuple):
    """
    This function describes the logic behind the /unban command.
    
    Args:
        message (Message): vkbottle message object.
        args (Tuple): tuple of command arguments.
    """

    if message.fwd_messages:
        return

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
        "command_name": "unban",
        "now_time": converter.now(),
    }

    if len(args) == 0 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await informer.user_name(
            message.reply_message.from_id, tag=False
        )
        context["target_nametag"] = await informer.user_name(
            message.reply_message.from_id, tag=True
        )

    elif len(args) == 1 and not message.reply_message:
        cuid = await get_cuid(args[0])
        if cuid is None:
            print("Command aborted: Wrong mention")
            return

        context["target_id"] = cuid
        context["target_name"] = await informer.user_name(cuid, tag=False)
        context["target_nametag"] = await informer.user_name(cuid, tag=True)

    else:
        return

    await com_processor.unban_proc(context)
