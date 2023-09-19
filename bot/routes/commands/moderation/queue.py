from bot.routes.commands.core import *
from bot.src_config import PERMISSION_ACCESS
from bot.usr_config import ALIASES, PREFIXES, QUEUE_TIME
from vkbottle.bot import Message
from typing import Tuple
from bot.routes.rules import *


@bl.chat_message(
    HandleCommand(ALIASES['queue'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['queue']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def queue(message: Message, args: Tuple):
    if message.fwd_messages:
        return

    delta = QUEUE_TIME

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
        "command_name": "queue",
        "now_time": converter.now(),
        "target_time": converter.now() + delta,
        "cmids": None
    }

    if len(args) == 0 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await informer.user_name(message.reply_message.from_id, tag=False)
        context["target_nametag"] = await informer.user_name(message.reply_message.from_id, tag=True)
        context["cmids"] = [message.reply_message.conversation_message_id]

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

    await com_processor.queue_proc(context, log=True, respond=False)


@bl.chat_message(
    HandleCommand(ALIASES['unqueue'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['unqueue']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unqueue(message: Message, args: Tuple):
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
        "command_name": "unqueue",
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

    await com_processor.unqueue_proc(context, log=True, respond=False)
