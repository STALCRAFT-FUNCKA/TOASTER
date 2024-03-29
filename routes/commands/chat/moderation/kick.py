"""
File with /kick and /terminate bot command.
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
    HandleCommand(ALIASES['terminate'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['terminate']),
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def terminate(message: Message, args: Tuple):
    """
    This function describes the logic behind the /terminate command.
    
    Args:
        message (Message): vkbottle message object.
        args (Tuple): tuple of command arguments.
    """

    if message.fwd_messages:
        return

    context = {
        "peer_id": message.peer_id,
        "peer_name": "Все беседы",
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await informer.user_name(message.from_id, tag=False),
        "initiator_nametag": await informer.user_name(message.from_id, tag=True),
        "target_id": None,
        "target_name": None,
        "target_nametag": None,
        "command_name": "terminate",
        "now_time": converter.now(),
        "cmids": None
    }

    collapse = False

    if len(args) == 0 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await informer.user_name(
            message.reply_message.from_id, tag=False
        )
        context["target_nametag"] = await informer.user_name(
            message.reply_message.from_id, tag=True
        )
        context["cmids"] = [message.reply_message.conversation_message_id]
        collapse = True

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

    await com_processor.terminate_proc(context, collapse=collapse)


@bl.chat_message(
    HandleCommand(ALIASES['kick'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['kick']),
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def kick(message: Message, args: Tuple):
    """
    This function describes the logic behind the /terminate command.
    
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
        "command_name": "kick",
        "now_time": converter.now(),
        "cmids": None
    }

    collapse = False

    if len(args) == 0 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await informer.user_name(
            message.reply_message.from_id, tag=False
        )
        context["target_nametag"] = await informer.user_name(
            message.reply_message.from_id, tag=True
        )
        context["cmids"] = [message.reply_message.conversation_message_id]
        collapse = True

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

    await com_processor.kick_proc(context, collapse=collapse)
