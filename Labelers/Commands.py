import time
from typing import Tuple

from vkbottle.bot import Bot, BotLabeler, Message
from DataBase.Utils import Connection
from Config import ALIASES, TOKEN, GROUP, SETTINGS, PERMISSION_LVL
from Logger.Logger import Logger
from Rules.CustomRules import (HandleCommand, CollapseCommand, AnswerCommand, CheckPermission, HandleIn, OnlyEnrolled,
                               IgnorePermission)


bot = Bot(token=TOKEN)
database = Connection('DataBase/database.db')
logger = Logger()
bl = BotLabeler()


"""
------------------------------------------------------------------------------------------------------------------------
Команда вывода справки\справочной информации.
"""
@bl.chat_message(
    HandleCommand(ALIASES['reference'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=1), # Moderator
    HandleIn(handle_log=True, handle_chat=True)
)
async def reference(message: Message):
    url = 'https://github.com/Oidaho/FUNCKA-BOT/blob/master/README.md'

    title = f'Перейдя по этой ссылке, вы сможете найти документацию на GitHub:\n {url}'
    await message.answer(title)


"""
------------------------------------------------------------------------------------------------------------------------
Команда регистрации беседы. 
Бот не будет производить никаких действий в беседе, пока она не будет зарегистрирована.
"""
@bl.chat_message(
    HandleCommand(ALIASES['enroll'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0), # Admin
    HandleIn(handle_log=False, handle_chat=True)
)
async def enroll(message: Message):
    # TODO: Логи
    PeerID = message.peer_id
    Destination = "CHAT"

    Peer_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=PeerID)
    PeerName = Peer_info.items[0].chat_settings.title

    if database.get_conversation(PeerID=PeerID, Destination=Destination):
        title = f"Данные беседы обновлены."

    else:
        title = f"Беседа зарегистрирована."

    await message.answer(title)

    database.add_conversation(PeerID=PeerID, PeerName=PeerName, Destination=Destination)
    for setting in SETTINGS:
        database.add_setting(PeerID=PeerID, SettingName=setting, SettingStatus=SETTINGS[setting])


@bl.chat_message(
    HandleCommand(ALIASES['drop'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0), # Admin
    HandleIn(handle_log=False, handle_chat=True)
)
async def drop(message: Message):
    PeerID = message.peer_id
    Destination = "CHAT"

    if database.get_conversation(PeerID=PeerID, Destination=Destination):
        title = f"Регистрация данной беседы упразднена."

        database.remove_conversation(PeerID=PeerID)

    else:
        title = f"Данная беседа не зарегистрирована."

    await message.answer(title)


"""
------------------------------------------------------------------------------------------------------------------------
Команда регистрации лог-чата. 
Таких лог-чатов может быть несколько.
Бот отправляет логи своих действий в каждый из помеченных этой командой чатов.
"""
@bl.chat_message(
    HandleCommand(ALIASES['enroll_log'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0), # Admin
    HandleIn(handle_log=True, handle_chat=False)
)
async def enroll_log(message: Message):
    PeerID = message.peer_id
    Destination = "LOG"

    Peer_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    PeerName = Peer_info.items[0].chat_settings.title

    if database.get_conversation(PeerID=PeerID, Destination=Destination):
        title = f"Данные беседы обновлены."

    else:
        title = f"Беседа назначена в качестве лог-чата."

    await message.answer(title)

    database.add_conversation(PeerID=PeerID, PeerName=PeerName, Destination=Destination)


@bl.chat_message(
    HandleCommand(ALIASES['drop_log'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0), # Admin
    HandleIn(handle_log=True, handle_chat=False)
)
async def drop_log(message: Message):
    PeerID = message.peer_id
    Destination = "LOG"

    if database.get_conversation(PeerID=PeerID, Destination=Destination):
        title = f"Данный лог-чат упразднён."

        database.remove_conversation(PeerID=PeerID)

    else:
        title = f"Беседа не является лог-чатом."

    await message.answer(title)


"""
------------------------------------------------------------------------------------------------------------------------
Команда, устанавливающая группу прав пользователю в беседе. 
"""
@bl.chat_message(
    HandleCommand(ALIASES['permission'], ['!', '/'], 1),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0), # Admin
    HandleIn(handle_log=True, handle_chat=True),
    OnlyEnrolled()
)
async def permission(message: Message, args: Tuple[str]):
    PeerID = message.peer_id
    UserID = message.reply_message.from_id

    UserInfo = await bot.api.users.get(UserID)
    UserName = f"{UserInfo[0].first_name} {UserInfo[0].last_name}"
    UserURL = f"https://vk.com/id{UserID}"

    PermissionLvl = int(args[0])
    PermissionName = PERMISSION_LVL[PermissionLvl]

    database.set_permission(UserID, UserName, UserURL, PermissionLvl, PermissionName, PeerID)


"""
------------------------------------------------------------------------------------------------------------------------
Команда кика пользователя с беседы. 
Бессрочно исключает пользователя из беседы.
"""
@bl.chat_message(
    HandleCommand(ALIASES['kick'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=1), # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def kick(message: Message):
    PeerID = Message.peer_id
    UserID = message.reply_message.from_id
    KickedByID = message.from_id

    if not database.get_kick(PeerID=PeerID, UserID=UserID):
        UserInfo = await bot.api.users.get(UserID)
        KickedByInfo = await bot.api.users.get(KickedByID)

        UserName = f"{UserInfo[0].first_name} {UserInfo[0].last_name}"
        UserURL = f"https://vk.com/id{UserID}"

        KickedByName = KickedByInfo[0].first_name + KickedByInfo[0].last_name
        KickedByURL = KickedByInfo[0].nickname

        KickTime = int(time.time())

        title = f""
        # TODO: Вывод в общий чат о кике
        await message.answer(title)

        database.add_kick(PeerID, UserID, UserName, UserURL, KickedByID, KickedByName, KickedByURL, KickTime)
        await bot.api.messages.remove_chat_user(message.chat_id, message.reply_message.from_id)


"""
------------------------------------------------------------------------------------------------------------------------
Команда блокировки пользователя в беседе. 
Временно исключает пользователя из беседы.
"""
@bl.chat_message(
    HandleCommand(ALIASES['ban'], ['!', '/'], 2),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=1), # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def ban(message: Message, args: Tuple[str]):
    pass # TODO: Сделать код

@bl.chat_message(
    HandleCommand(ALIASES['unban'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=1), # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unban(message: Message):
    pass # TODO: Сделать код


"""
------------------------------------------------------------------------------------------------------------------------
Команда заглушения пользователя в беседе. 
Временно не позволяет пользователю писать сообщения.
"""
@bl.chat_message(
    HandleCommand(ALIASES['mute'], ['!', '/'], 2),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=1), # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def mute(message: Message, args: Tuple[str]):
    pass # TODO: Сделать код

@bl.chat_message(
    HandleCommand(ALIASES['unmute'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=1), # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unmute(message: Message):
    pass # TODO: Сделать код


"""
------------------------------------------------------------------------------------------------------------------------
Команда предупреждения пользователя в беседе. 
Выдает пользователю одно временное предупреждение (* из 3).
"""
@bl.chat_message(
    HandleCommand(ALIASES['warn'], ['!', '/'],  0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=1), # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def warn(message: Message):
    pass # TODO: Сделать код

@bl.chat_message(
    HandleCommand(ALIASES['unwarn'], ['!', '/'],  0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=1), # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unwarn(message: Message):
    pass # TODO: Сделать код

"""
------------------------------------------------------------------------------------------------------------------------
Команда удаляет сообщение(я) пользователя в беседе. 
"""
@bl.chat_message(
    HandleCommand(ALIASES['delete'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=True),
    CheckPermission(access_to=1), # Moderator
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def delete(message: Message):
    async def _collapse(m: Message):
        MessageID = m.conversation_message_id
        PeerID = message.peer_id
        try:
            await bot.api.messages.delete(group_id=GROUP, peer_id=PeerID, cmids=MessageID, delete_for_all=True)

        except Exception:
            ...

    if message.fwd_messages:
        # TODO: Вывод лога при удалении в лог-чат
        for msg in message.fwd_messages:
            await _collapse(msg)

    else:
        # TODO: Вывод лога при удалении в лог-чат
        await _collapse(message.reply_message)


"""
------------------------------------------------------------------------------------------------------------------------
Команда копирует сообщение пользователя в беседе и отправляет от лица бота. 
"""
@bl.chat_message(
    HandleCommand(ALIASES['copy'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=1), # Moderator
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def copy(message: Message):
    title = message.reply_message.text
    await message.answer(title)
    # TODO: Вывод лога в лог-чат