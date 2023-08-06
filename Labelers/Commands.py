import time
from typing import Tuple

from vkbottle.bot import Bot, BotLabeler, Message
from DataBase.Utils import Connection
from Config import ALIASES, TOKEN, GROUP, SETTINGS, PERMISSION_LVL, TIME_COEFFICENT
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
    HandleIn(handle_log=True, handle_chat=False)
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
    def _log():
        ...

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
    def _log():
        ...

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
    def _log():
        ...

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
    def _log():
        ...

    async def _say(title):
        await message.answer(title)

    PeerID = message.peer_id
    Destination = "LOG"

    if database.get_conversation(PeerID=PeerID, Destination=Destination):
        await _say("Данный лог-чат упразднён.")
        database.remove_conversation(PeerID=PeerID)

    else:
        await _say("Беседа не является лог-чатом.")




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
    def _log():
        ...

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
    def _log():
        ...

    async def _say():
        title = f""
        # TODO: Вывод в общий чат о наказании
        await message.answer(title)

    PeerID = Message.peer_id
    UserID = message.reply_message.from_id
    KickedByID = message.from_id

    if not database.get_kick(PeerID=PeerID, UserID=UserID):
        UserInfo = await bot.api.users.get(UserID)
        KickedByInfo = await bot.api.users.get(KickedByID)

        UserName = f"{UserInfo[0].first_name} {UserInfo[0].last_name}"
        UserURL = f"https://vk.com/id{UserID}"

        KickedByName = f"{KickedByInfo[0].first_name} {KickedByInfo[0].last_name}"
        KickedByURL = f"https://vk.com/id{KickedByID}"

        KickTime = int(time.time())

        await _say()
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
    def _log():
        ...

    async def _say():
        title = f""
        # TODO: Вывод в общий чат о наказании
        await message.answer(title)

    PeerID = Message.peer_id
    UserID = message.reply_message.from_id
    BannedByID = message.from_id

    try:
        BanDeltaTime = (int(args[0]) * TIME_COEFFICENT[args[1]]) if args[0] != 0 \
            else (int(args[0]) + 1 * TIME_COEFFICENT[args[1]])

    except Exception:
        return

    if not database.get_kick(PeerID=PeerID, UserID=UserID):
        UserInfo = await bot.api.users.get(UserID)
        BannedByInfo = await bot.api.users.get(BannedByID)

        UserName = f"{UserInfo[0].first_name} {UserInfo[0].last_name}"
        UserURL = f"https://vk.com/id{UserID}"

        BannedByName = f"{BannedByInfo[0].first_name} {BannedByInfo[0].last_name}"
        BannedByURL = f"https://vk.com/id{BannedByInfo}"

        BanTime = int(time.time())
        UnbanTime = BanTime + BanDeltaTime

        await _say()
        database.add_ban(PeerID, UserID, UserName, UserURL, BannedByID, BannedByName, BannedByURL, BanTime, UnbanTime)
        await bot.api.messages.remove_chat_user(message.chat_id, message.reply_message.from_id)


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
    def _log():
        ...

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
    def _log():
        ...

    async def _say():
        title = f""
        # TODO: Вывод в общий чат о наказании
        await message.answer(title)

    PeerID = Message.peer_id
    UserID = message.reply_message.from_id
    MutedByID = message.from_id

    try:
        MuteDeltaTime = (int(args[0]) * TIME_COEFFICENT[args[1]]) if args[0] != 0 \
            else (int(args[0]) + 1 * TIME_COEFFICENT[args[1]])

    except Exception:
        return

    if not database.get_kick(PeerID=PeerID, UserID=UserID):
        UserInfo = await bot.api.users.get(UserID)
        MutedByInfo = await bot.api.users.get(MutedByID)

        UserName = f"{UserInfo[0].first_name} {UserInfo[0].last_name}"
        UserURL = f"https://vk.com/id{UserID}"

        MutedByName = f"{MutedByInfo[0].first_name} {MutedByInfo[0].last_name}"
        MutedByURL = f"https://vk.com/id{MutedByID}"

        MuteTime = int(time.time())
        UnmuteTime = MuteTime + MuteDeltaTime

        await _say()
        database.add_mute(PeerID, UserID, UserName, UserURL, MutedByID, MutedByName, MutedByURL, MuteTime, UnmuteTime)

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
    def _log():
        ...

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
    def _log():
        ...

    async def _say():
        title = f""
        # TODO: Вывод в общий чат о наказании
        await message.answer(title)

    PeerID = Message.peer_id
    UserID = message.reply_message.from_id
    WarnedByID = message.from_id

    UserInfo = await bot.api.users.get(UserID)
    WarnedByInfo = await bot.api.users.get(WarnedByID)

    UserName = f"{UserInfo[0].first_name} {UserInfo[0].last_name}"
    UserURL = f"https://vk.com/id{UserID}"

    WarnedByName = f"{WarnedByInfo[0].first_name} {WarnedByInfo[0].last_name}"
    WarnedByURL = f"https://vk.com/id{WarnedByInfo}"

    WarnTime = int(time.time())
    UnwarnTime = WarnTime + TIME_COEFFICENT["d"]

    WarnCount = database.get_warn(PeerID=PeerID, UserID=UserID) + 1

    await _say()
    database.add_warn(PeerID, UserID, UserName, UserURL,
                      WarnedByID, WarnedByName, WarnedByURL,
                      WarnTime, UnwarnTime, WarnCount)



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
    def _log():
        ...

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
    def _log():
        ...

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
    def _log():
        ...

    title = message.reply_message.text
    await message.answer(title)
    # TODO: Вывод лога в лог-чат