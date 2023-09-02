from typing import Tuple
from vkbottle.bot import BotLabeler, Message
from database import Processor
from config import ALIASES, PREFIXES, PERMISSION_LVL
from utils import *
from rules import *

bl = BotLabeler()

info = Info()
converter = Converter()
processor = Processor()

"""
------------------------------------------------------------------------------------------------------------------------
Команда кика пользователя со ВСЕХ бесед. 
Бессрочно исключает пользователя из  ВСЕХ бесед.
"""


@bl.chat_message(
    HandleCommand(ALIASES['terminate'], PREFIXES, 1),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Administrator
    IgnoreMention(ignore_from=1),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def terminate(message: Message, args: Tuple[str]):
    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await info.user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[0])
    if cuid is None:
        print("Command aborted: Wrong mention")
        return

    context = {
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "target_id": cuid,
        "target_name": await info.user_name(cuid, tag=False),
        "target_nametag": await info.user_name(cuid, tag=True),
        "command_name": "terminate",
        "now_time": converter.now(),
    }

    await processor.terminate_proc(context, log=True, respond=True)


"""
------------------------------------------------------------------------------------------------------------------------
Команда, устанавливающая группу прав пользователю в беседе. 
"""


@bl.chat_message(
    HandleCommand(ALIASES['permission'], PREFIXES, 2),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Admin
    IgnoreMention(ignore_from=1),
    HandleIn(handle_log=True, handle_chat=True),
    OnlyEnrolled()
)
async def permission(message: Message, args: Tuple[str]):
    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await info.user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[1])
    if cuid is None:
        print("Command aborted: Wrong mention")
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
        "peer_name": "Все беседы",
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "target_id": cuid,
        "target_name": await info.user_name(cuid, tag=False),
        "target_nametag": await info.user_name(cuid, tag=True),
        "target_lvl": lvl,
        "command_name": "permission",
        "now_time": converter.now(),
    }

    await processor.kick_proc(context, log=True, respond=True)


"""
------------------------------------------------------------------------------------------------------------------------
Команда кика пользователя с беседы. 
Бессрочно исключает пользователя из беседы.
"""


@bl.chat_message(
    HandleCommand(ALIASES['kick'], PREFIXES, 1),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    IgnoreMention(ignore_from=1),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def kick(message: Message, args: Tuple[str]):
    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await info.user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[0])
    if cuid is None:
        print("Command aborted: Wrong mention")
        return

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "target_id": cuid,
        "target_name": await info.user_name(cuid, tag=False),
        "target_nametag": await info.user_name(cuid, tag=True),
        "command_name": "kick",
        "now_time": converter.now(),
    }

    await processor.kick_proc(context, log=True, respond=True)

"""
------------------------------------------------------------------------------------------------------------------------
Команда блокировки пользователя в беседе. 
Временно исключает пользователя из беседы.
"""


@bl.chat_message(
    HandleCommand(ALIASES['ban'], PREFIXES, 3),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    IgnoreMention(ignore_from=1),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def ban(message: Message, args: Tuple[str]):
    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await info.user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[2])
    if cuid is None:
        print("Command aborted: Wrong mention")
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
        "target_id": cuid,
        "target_name": await info.user_name(cuid, tag=False),
        "target_nametag": await info.user_name(cuid, tag=True),
        "command_name": "ban",
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficent),
    }

    await processor.ban_proc(context, log=True, respond=True)


@bl.chat_message(
    HandleCommand(ALIASES['unban'], PREFIXES, 1),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    IgnoreMention(ignore_from=1),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unban(message: Message, args: Tuple[str]):
    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await info.user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[0])
    if cuid is None:
        print("Command aborted: Wrong mention")
        return

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "target_id": cuid,
        "target_name": await info.user_name(cuid, tag=False),
        "target_nametag": await info.user_name(cuid, tag=True),
        "command_name": "unban",
        "now_time": converter.now(),
    }

    await processor.unban_proc(context, log=True, respond=False)


"""
------------------------------------------------------------------------------------------------------------------------
Команда заглушения пользователя в беседе. 
Временно не позволяет пользователю писать сообщения.
"""


@bl.chat_message(
    HandleCommand(ALIASES['mute'], PREFIXES, 3),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    IgnoreMention(ignore_from=1),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def mute(message: Message, args: Tuple[str]):
    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await info.user_id(screen_name=screen_name)
        return uid

    cuid = await get_cuid(args[2])
    if cuid is None:
        print("Command aborted: Wrong mention")
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
        "target_id": cuid,
        "target_name": await info.user_name(cuid, tag=False),
        "target_nametag": await info.user_name(cuid, tag=True),
        "command_name": "mute",
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficent),
    }

    await processor.mute_proc(context, log=True, respond=True)


@bl.chat_message(
    HandleCommand(ALIASES['unmute'], PREFIXES, 1),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    IgnoreMention(ignore_from=1),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unmute(message: Message, args: Tuple[str]):
    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await info.user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[0])
    if cuid is None:
        print("Command aborted: Wrong mention")
        return

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "target_id": cuid,
        "target_name": await info.user_name(cuid, tag=False),
        "target_nametag": await info.user_name(cuid, tag=True),
        "command_name": "unmute",
        "now_time": converter.now(),
    }

    await processor.unmute_proc(context, log=True, respond=False)


"""
------------------------------------------------------------------------------------------------------------------------
Команда предупреждения пользователя в беседе. 
Выдает пользователю одно временное предупреждение (* из 3).
"""


@bl.chat_message(
    HandleCommand(ALIASES['warn'], PREFIXES, 1),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    IgnoreMention(ignore_from=1),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def warn(message: Message, args: Tuple[str]):
    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await info.user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[0])
    if cuid is None:
        print("Command aborted: Wrong mention")
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
        "target_id": cuid,
        "target_name": await info.user_name(cuid, tag=False),
        "target_nametag": await info.user_name(cuid, tag=True),
        "command_name": "warn",
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficent),
    }

    await processor.warn_proc(context, log=True, respond=True)


@bl.chat_message(
    HandleCommand(ALIASES['unwarn'], PREFIXES, 1),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    IgnoreMention(ignore_from=1),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unwarn(message: Message, args: Tuple[str]):
    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await info.user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[0])
    if cuid is None:
        print("Command aborted: Wrong mention")
        return

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await info.user_name(message.from_id, tag=False),
        "initiator_nametag": await info.user_name(message.from_id, tag=True),
        "target_id": cuid,
        "target_name": await info.user_name(cuid, tag=False),
        "target_nametag": await info.user_name(cuid, tag=True),
        "command_name": "unwarn",
        "now_time": converter.now(),
    }

    await processor.unwarn_proc(context, log=True, respond=True)
