from ..core import *
from src_config import PERMISSION_ACCESS
from usr_config import ALIASES, PREFIXES
from vkbottle.bot import Message
from typing import Tuple
from routes.rules import *


@bl.chat_message(
    HandleCommand(ALIASES['mute'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['mute']),
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def mute(message: Message, args: Tuple):
    if not args or message.fwd_messages:
        return

    try:
        time = int(args[0])
        coefficient = args[1]
    except Exception as error:
        print("Wrong args format. Setting default punish time: ", error)
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
        "command_name": "mute",
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficient),
        "cmids": None
    }

    collapse = False

    if len(args) == 2 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await informer.user_name(message.reply_message.from_id, tag=False)
        context["target_nametag"] = await informer.user_name(message.reply_message.from_id, tag=True)
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

    await com_processor.mute_proc(context, collapse=collapse, log=True, respond=True)


@bl.chat_message(
    HandleCommand(ALIASES['unmute'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['unmute']),
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unmute(message: Message, args: Tuple):
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
        "command_name": "unmute",
        "now_time": converter.now(),
    }

    if len(args) == 0 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await informer.user_name(message.reply_message.from_id, tag=False)
        context["target_nametag"] = await informer.user_name(message.reply_message.from_id, tag=True)

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

    await com_processor.unmute_proc(context, log=True, respond=False)
