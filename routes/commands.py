from config import ALIASES, PREFIXES, PERMISSION_LVL, PERMISSION_ACCESS, QUEUE_TIME
from vkbottle.bot import BotLabeler, Message
from database.proc import CommandProcessor
from typing import Tuple
from utils import *
from .rules import *


bl = BotLabeler()

info = Info()
converter = Converter()
processor = CommandProcessor()


async def get_cuid(arg):
    screen_name = arg.replace("@", "")
    screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
    uid = await info.user_id(screen_name=screen_name)
    return uid

"""
------------------------------------------------------------------------------------------------------------------------
Команда регистрации беседы. 
Бот не будет производить никаких действий в беседе, пока она не будет зарегистрирована.
"""


@bl.chat_message(
    HandleCommand(ALIASES['mark'], PREFIXES, 1),
    CollapseCommand(),
    AllowAnswer(allow_reply=False, allow_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['mark']),
    HandleIn(handle_log=False, handle_chat=True)
)
async def mark(message: Message, args: Tuple):

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "peer_type": None,
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "command_name": None,
        "now_time": converter.now(),
    }

    if args[0] == "chat":
        context["peer_type"] = "CHAT"
        context["command_name"] = "mark chat"
        await processor.chat_proc(context, log=True, respond=True)

    if args[0] == "log":
        context["peer_type"] = "LOG"
        context["command_name"] = "mark log"
        await processor.log_proc(context, log=True, respond=True)

    if args[0] == "drop":
        context["command_name"] = "mark drop"
        await processor.drop_proc(context, log=True, respond=True)


"""
------------------------------------------------------------------------------------------------------------------------
Команда, устанавливающая группу прав пользователю в беседе. 
"""


@bl.chat_message(
    HandleCommand(ALIASES['permission'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['permission']),
    HandleIn(handle_log=True, handle_chat=True),
    OnlyEnrolled()
)
async def permission(message: Message, args: Tuple[str]):
    if not args or message.fwd_messages:
        return

    try:
        lvl = int(args[0])
        if lvl not in PERMISSION_LVL.keys():
            lvl = 0
    except Exception as error:
        print("Setting standard lvl: ", error)
        lvl = 0

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "target_id": None,
        "target_name": None,
        "target_nametag": None,
        "target_lvl": lvl,
        "command_name": "permission",
        "now_time": converter.now(),
    }

    if len(args) == 1 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await info.user_name(message.reply_message.from_id, tag=False)
        context["target_nametag"] = await info.user_name(message.reply_message.from_id, tag=True)

    elif len(args) == 2 and not message.reply_message:
        cuid = await get_cuid(args[1])
        if cuid is None:
            print("Command aborted: Wrong mention")
            return

        context["target_id"] = cuid
        context["target_name"] = await info.user_name(cuid, tag=False)
        context["target_nametag"] = await info.user_name(cuid, tag=True)

    else:
        return

    await processor.permission_proc(context, log=True, respond=False)


"""
------------------------------------------------------------------------------------------------------------------------
Команда кика пользователя со ВСЕХ бесед. 
Бессрочно исключает пользователя из  ВСЕХ бесед.
"""


@bl.chat_message(
    HandleCommand(ALIASES['terminate'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['terminate']),
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def terminate(message: Message, args: Tuple):
    if message.fwd_messages:
        return

    context = {
        "peer_name": "Все беседы",
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
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
        context["target_name"] = await info.user_name(message.reply_message.from_id, tag=False)
        context["target_nametag"] = await info.user_name(message.reply_message.from_id, tag=True)
        context["cmids"] = [message.reply_message.conversation_message_id]
        collapse = True

    elif len(args) == 1 and not message.reply_message:
        cuid = await get_cuid(args[0])
        if cuid is None:
            print("Command aborted: Wrong mention")
            return

        context["target_id"] = cuid
        context["target_name"] = await info.user_name(cuid, tag=False)
        context["target_nametag"] = await info.user_name(cuid, tag=True)

    else:
        return

    await processor.terminate_proc(context, collapse=collapse, log=True, respond=True)


"""
------------------------------------------------------------------------------------------------------------------------
Команда кика пользователя с беседы. 
Бессрочно исключает пользователя из беседы.
"""


@bl.chat_message(
    HandleCommand(ALIASES['kick'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['kick']),
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def kick(message: Message, args: Tuple):
    if message.fwd_messages:
        return

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
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
        context["target_name"] = await info.user_name(message.reply_message.from_id, tag=False)
        context["target_nametag"] = await info.user_name(message.reply_message.from_id, tag=True)
        context["cmids"] = [message.reply_message.conversation_message_id]
        collapse = True

    elif len(args) == 1 and not message.reply_message:
        cuid = await get_cuid(args[0])
        if cuid is None:
            print("Command aborted: Wrong mention")
            return

        context["target_id"] = cuid
        context["target_name"] = await info.user_name(cuid, tag=False)
        context["target_nametag"] = await info.user_name(cuid, tag=True)

    else:
        return

    await processor.kick_proc(context, collapse=collapse, log=True, respond=True)


"""
------------------------------------------------------------------------------------------------------------------------
Команда блокировки пользователя в беседе. 
Временно исключает пользователя из беседы.
"""


@bl.chat_message(
    HandleCommand(ALIASES['ban'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['ban']),
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def ban(message: Message, args: Tuple):
    if not args or message.fwd_messages:
        return

    try:
        time = int(args[0])
        coefficent = args[1]
    except Exception as error:
        print("Wrong args format. Setting default punish time: ", error)
        time = 1
        coefficent = "h"

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "target_id": None,
        "target_name": None,
        "target_nametag": None,
        "command_name": "ban",
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficent),
        "cmids": None
    }

    collapse = False

    if len(args) == 2 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await info.user_name(message.reply_message.from_id, tag=False)
        context["target_nametag"] = await info.user_name(message.reply_message.from_id, tag=True)
        context["cmids"] = [message.reply_message.conversation_message_id]
        collapse = True

    elif len(args) == 3 and not message.reply_message:
        cuid = await get_cuid(args[2])
        if cuid is None:
            print("Command aborted: Wrong mention")
            return

        context["target_id"] = cuid
        context["target_name"] = await info.user_name(cuid, tag=False)
        context["target_nametag"] = await info.user_name(cuid, tag=True)

    else:
        return

    await processor.ban_proc(context, collapse=collapse, log=True, respond=True)


@bl.chat_message(
    HandleCommand(ALIASES['unban'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['unban']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unban(message: Message, args: Tuple):
    if message.fwd_messages:
        return

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "target_id": None,
        "target_name": None,
        "target_nametag": None,
        "command_name": "unban",
        "now_time": converter.now(),
    }

    if len(args) == 0 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await info.user_name(message.reply_message.from_id, tag=False)
        context["target_nametag"] = await info.user_name(message.reply_message.from_id, tag=True)

    elif len(args) == 1 and not message.reply_message:
        cuid = await get_cuid(args[0])
        if cuid is None:
            print("Command aborted: Wrong mention")
            return

        context["target_id"] = cuid
        context["target_name"] = await info.user_name(cuid, tag=False)
        context["target_nametag"] = await info.user_name(cuid, tag=True)

    else:
        return

    await processor.unban_proc(context, log=True, respond=False)

"""
------------------------------------------------------------------------------------------------------------------------
Команда заглушения пользователя в беседе. 
Временно не позволяет пользователю писать сообщения.
"""


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
        coefficent = args[1]
    except Exception as error:
        print("Wrong args format. Setting default punish time: ", error)
        time = 1
        coefficent = "h"

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "target_id": None,
        "target_name": None,
        "target_nametag": None,
        "command_name": "mute",
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficent),
        "cmids": None
    }

    collapse = False

    if len(args) == 2 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await info.user_name(message.reply_message.from_id, tag=False)
        context["target_nametag"] = await info.user_name(message.reply_message.from_id, tag=True)
        context["cmids"] = [message.reply_message.conversation_message_id]
        collapse = True

    elif len(args) == 3 and not message.reply_message:
        cuid = await get_cuid(args[2])
        if cuid is None:
            print("Command aborted: Wrong mention")
            return

        context["target_id"] = cuid
        context["target_name"] = await info.user_name(cuid, tag=False)
        context["target_nametag"] = await info.user_name(cuid, tag=True)

    else:
        return

    await processor.mute_proc(context, collapse=collapse, log=True, respond=True)


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
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "target_id": None,
        "target_name": None,
        "target_nametag": None,
        "command_name": "unmute",
        "now_time": converter.now(),
    }

    if len(args) == 0 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await info.user_name(message.reply_message.from_id, tag=False)
        context["target_nametag"] = await info.user_name(message.reply_message.from_id, tag=True)

    elif len(args) == 1 and not message.reply_message:
        cuid = await get_cuid(args[0])
        if cuid is None:
            print("Command aborted: Wrong mention")
            return

        context["target_id"] = cuid
        context["target_name"] = await info.user_name(cuid, tag=False)
        context["target_nametag"] = await info.user_name(cuid, tag=True)

    else:
        return

    await processor.unmute_proc(context, log=True, respond=False)


"""
------------------------------------------------------------------------------------------------------------------------
Команда предупреждения пользователя в беседе. 
Выдает пользователю одно временное предупреждение (* из 3).
"""


@bl.chat_message(
    HandleCommand(ALIASES['warn'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['warn']),
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def warn(message: Message, args: Tuple):
    if message.fwd_messages:
        return

    time = 1
    coefficent = "d"

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "target_id": None,
        "target_name": None,
        "target_nametag": None,
        "command_name": "warn",
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficent),
        "cmids": None
    }

    collapse = False

    if len(args) == 0 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await info.user_name(message.reply_message.from_id, tag=False)
        context["target_nametag"] = await info.user_name(message.reply_message.from_id, tag=True)
        context["cmids"] = [message.reply_message.conversation_message_id]
        collapse = True

    elif len(args) == 1 and not message.reply_message:
        cuid = await get_cuid(args[0])
        if cuid is None:
            print("Command aborted: Wrong mention")
            return

        context["target_id"] = cuid
        context["target_name"] = await info.user_name(cuid, tag=False)
        context["target_nametag"] = await info.user_name(cuid, tag=True)

    else:
        return

    await processor.warn_proc(context, collapse=collapse, log=True, respond=True)


@bl.chat_message(
    HandleCommand(ALIASES['unwarn'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['unwarn']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unwarn(message: Message, args: Tuple):
    if message.fwd_messages:
        return

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "target_id": None,
        "target_name": None,
        "target_nametag": None,
        "command_name": "unwarn",
        "now_time": converter.now(),
    }

    if len(args) == 0 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await info.user_name(message.reply_message.from_id, tag=False)
        context["target_nametag"] = await info.user_name(message.reply_message.from_id, tag=True)

    elif len(args) == 1 and not message.reply_message:
        cuid = await get_cuid(args[0])
        if cuid is None:
            print("Command aborted: Wrong mention")
            return

        context["target_id"] = cuid
        context["target_name"] = await info.user_name(cuid, tag=False)
        context["target_nametag"] = await info.user_name(cuid, tag=True)

    else:
        return

    await processor.unwarn_proc(context, log=True, respond=True)


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
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
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
        context["target_name"] = await info.user_name(message.reply_message.from_id, tag=False)
        context["target_nametag"] = await info.user_name(message.reply_message.from_id, tag=True)
        context["cmids"] = [message.reply_message.conversation_message_id]

    elif len(args) == 1 and not message.reply_message:
        cuid = await get_cuid(args[0])
        if cuid is None:
            print("Command aborted: Wrong mention")
            return

        context["target_id"] = cuid
        context["target_name"] = await info.user_name(cuid, tag=False)
        context["target_nametag"] = await info.user_name(cuid, tag=True)

    else:
        return

    await processor.queue_proc(context, log=True, respond=False)


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
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "target_id": None,
        "target_name": None,
        "target_nametag": None,
        "command_name": "unqueue",
        "now_time": converter.now(),
    }

    if len(args) == 0 and message.reply_message:
        context["target_id"] = message.reply_message.from_id
        context["target_name"] = await info.user_name(message.reply_message.from_id, tag=False)
        context["target_nametag"] = await info.user_name(message.reply_message.from_id, tag=True)

    elif len(args) == 1 and not message.reply_message:
        cuid = await get_cuid(args[0])
        if cuid is None:
            print("Command aborted: Wrong mention")
            return

        context["target_id"] = cuid
        context["target_name"] = await info.user_name(cuid, tag=False)
        context["target_nametag"] = await info.user_name(cuid, tag=True)

    else:
        return

    await processor.unqueue_proc(context, log=True, respond=False)


"""
------------------------------------------------------------------------------------------------------------------------
Команда удаляет сообщение(я) пользователя в беседе. 
"""


@bl.chat_message(
    HandleCommand(ALIASES['delete'], PREFIXES, 0),
    CollapseCommand(),
    AllowAnswer(allow_reply=True, allow_fwd=True),
    CheckPermission(access_to=PERMISSION_ACCESS['delete']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def delete(message: Message):
    if message.reply_message is not None:
        cmids = [message.reply_message.conversation_message_id]
    else:
        cmids = [msg.conversation_message_id for msg in message.fwd_messages]

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "command_name": "delete",
        "now_time": converter.now(),
        "cmids": cmids,
    }

    await processor.delete_proc(context, log=True, respond=False)


"""
------------------------------------------------------------------------------------------------------------------------
Команда копирует сообщение пользователя в беседе и отправляет от лица бота. 
"""


@bl.chat_message(
    HandleCommand(ALIASES['copy'], PREFIXES, 0),
    CollapseCommand(),
    AllowAnswer(allow_reply=True, allow_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['copy']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def copy(message: Message):
    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "command_name": "copy",
        "now_time": converter.now(),
        "cmids": [message.reply_message.conversation_message_id],
        "copied": message.reply_message.text
    }

    await processor.copy_proc(context, log=True, respond=False)


"""
------------------------------------------------------------------------------------------------------------------------
Команда изменяет значение настроек в беседе. 
"""


@bl.chat_message(
    HandleCommand(ALIASES['setting'], PREFIXES, 2),
    CollapseCommand(),
    AllowAnswer(allow_reply=False, allow_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['setting']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def setting(message: Message, args: Tuple):
    setting_name = args[0]
    setting_status = args[1]

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "command_name": "setting",
        "setting_name": setting_name,
        "setting_status": setting_status,
        "now_time": converter.now()
    }

    await processor.setting_proc(context, log=True, respond=False)
