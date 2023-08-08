import time
from typing import Tuple

from vkbottle.bot import Bot, BotLabeler, Message

from DataBase.Interface import Connection
from Config import ALIASES, TOKEN, GROUP, SETTINGS, PERMISSION_LVL, TIME_COEFFICENT, STUFF_ADMIN_ID
from Logger.Logger import Logger
from Utils.InformationGetter import About
from Utils.TimeConverter import Converter
from Rules.CustomRules import (
    HandleCommand,
    CollapseCommand,
    AnswerCommand,
    CheckPermission,
    HandleIn,
    OnlyEnrolled,
    IgnorePermission
)


bot = Bot(token=TOKEN)
database = Connection('DataBase/database.db')
logger = Logger()
bl = BotLabeler()

About = About()
Converter = Converter()

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
    async def _say(title):
        await message.answer(title)

    url = "https://github.com/Oidaho/FUNCKA-BOT/blob/master/README.md"
    await _say(f"Перейдя по этой ссылке, вы сможете найти документацию на GitHub:\n {url}")


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
    async def _log():
        pl = database.get_permission(UserID=About.UserID(message), PeerID=About.PeerID(message))
        text = f"Инициатор: @id{About.UserID(message)} ({await About.UserFullName(message)})\n" \
               f"Роль: {pl} - {PERMISSION_LVL[pl]}\n" \
               f"Источник: {await About.PeerName(message)}\n" \
               f"Команда: /enroll \n" \
               f"Время (МСК): {Converter.convert(time.time())}"

        forward = {}

        return {'text': text, 'forward': forward}

    async def _say(title):
        await message.answer(title)

    PeerID = About.PeerID(message)
    Destination = "CHAT"

    PeerName = About.PeerName(message)

    if database.get_conversation(PeerID=PeerID, Destination=Destination):
        await _say("Данные беседы обновлены.")

    else:
        await _say(f"Беседа зарегистрирована.")

    await logger.send_log(await _log())
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
    async def _log():
        pl = database.get_permission(UserID=About.UserID(message), PeerID=About.PeerID(message))
        text = f"Инициатор: @id{About.UserID(message)} ({await About.UserFullName(message)})\n" \
               f"Роль: {pl} - {PERMISSION_LVL[pl]}\n" \
               f"Источник: {await About.PeerName(message)}\n" \
               f"Команда: /drop \n" \
               f"Время (МСК): {Converter.convert(time.time())}"

        forward = {}

        return {'text': text, 'forward': forward}

    async def _say(title):
        await message.answer(title)

    PeerID = About.PeerID(message)
    Destination = "CHAT"

    if database.get_conversation(PeerID=PeerID, Destination=Destination):
        await _say("Регистрация данной беседы упразднена.")

        await logger.send_log(await _log())
        database.remove_conversation(PeerID=PeerID)

    else:
        await _say("Данная беседа не зарегистрирована.")


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
    async def _log():
        pl = database.get_permission(UserID=About.UserID(message), PeerID=About.PeerID(message))
        text = f"Инициатор: @id{About.UserID(message)} ({await About.UserFullName(message)})\n" \
               f"Роль: {pl} - {PERMISSION_LVL[pl]}\n" \
               f"Источник: {await About.PeerName(message)}\n" \
               f"Команда: /enroll_log \n" \
               f"Время (МСК): {Converter.convert(time.time())}"

        forward = {}

        return {'text': text, 'forward': forward}

    async def _say(title):
        await message.answer(title)

    PeerID = About.PeerID(message)
    Destination = "LOG"

    PeerName = About.PeerName(message)

    if database.get_conversation(PeerID=PeerID, Destination=Destination):
        await _say("Данные беседы обновлены.")

    else:
        await _say("Беседа назначена в качестве лог-чата.")

    await logger.send_log(await _log())
    database.add_conversation(PeerID=PeerID, PeerName=PeerName, Destination=Destination)


@bl.chat_message(
    HandleCommand(ALIASES['drop_log'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0), # Admin
    HandleIn(handle_log=True, handle_chat=False)
)
async def drop_log(message: Message):
    async def _log():
        pl = database.get_permission(UserID=About.UserID(message), PeerID=About.PeerID(message))
        text = f"Инициатор: @id{About.UserID(message)} ({await About.UserFullName(message)})\n" \
               f"Роль: {pl} - {PERMISSION_LVL[pl]}\n" \
               f"Источник: {await About.PeerName(message)}\n" \
               f"Команда: /drop_log \n" \
               f"Время (МСК): {Converter.convert(time.time())}"

        forward = {}

        return {'text': text, 'forward': forward}

    async def _say(title):
        await message.answer(title)

    PeerID = About.PeerID(message)
    Destination = "LOG"

    if database.get_conversation(PeerID=PeerID, Destination=Destination):
        await _say("Данный лог-чат упразднён.")

        await logger.send_log(await _log())
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
    async def _log():
        pl = database.get_permission(UserID=About.UserID(message), PeerID=About.PeerID(message))
        text = f"Инициатор: @id{About.UserID(message)} ({await About.UserFullName(message)})\n" \
               f"Роль: {pl} - {PERMISSION_LVL[pl]}\n" \
               f"Источник: {await About.PeerName(message)}\n" \
               f"Команда: /permission\n" \
               f"Уровень прав: {int(args[0])} - {PERMISSION_LVL[int(args[0])]}\n" \
               f"Цель: @id{About.UserID(message.reply_message)} ({await About.UserFullName(message.reply_message)})\n" \
               f"Время (МСК): {Converter.convert(time.time())}"

        forward = {}

        return {'text': text, 'forward': forward}

    PeerID = About.PeerID(message)
    UserID = About.UserID(message.reply_message)

    UserName = About.UserFullName(message.reply_message)
    UserURL = About.UserURL(message.reply_message)

    try:
        PermissionLvl = int(args[0])
        PermissionName = PERMISSION_LVL[PermissionLvl]

        await logger.send_log(await _log())
        database.set_permission(UserID, UserName, UserURL, PermissionLvl, PermissionName, PeerID)

    except Exception:
        ...


"""
------------------------------------------------------------------------------------------------------------------------
Команда кика пользователя с беседы. 
Бессрочно исключает пользователя из беседы.
"""
@bl.chat_message(
    HandleCommand(ALIASES['kick'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0), # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def kick(message: Message):
    async def _log():
        pl = database.get_permission(UserID=About.UserID(message), PeerID=About.PeerID(message))
        text = f"Инициатор: @id{About.UserID(message)} ({await About.UserFullName(message)})\n" \
               f"Роль: {pl} - {PERMISSION_LVL[pl]}\n" \
               f"Источник: {await About.PeerName(message)}\n" \
               f"Команда: /kick \n" \
               f"Цель: @id{About.UserID(message.reply_message)} ({await About.UserFullName(message.reply_message)})\n" \
               f"Время (МСК): {Converter.convert(time.time())}"

        forward = {
            'peer_id': About.PeerID(message),
            'conversation_message_ids': [About.CvsMessageID(message.reply_message)]
        }

        return {'text': text, 'forward': forward}

    async def _say():
        title = f"@id{About.UserID(message.reply_message)} (Пользователь) исключен из беседы навсегда.\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    PeerID = About.PeerID(message)
    UserID = About.UserID(message.reply_message)
    KickedByID = About.UserID(message)

    if not database.get_kick(PeerID=PeerID, UserID=UserID):
        UserName = About.UserFullName(message.reply_message)
        UserURL = About.UserURL(message.reply_message)

        KickedByName = About.UserFullName(message)
        KickedByURL = About.UserURL(message)

        KickTime = int(time.time())

        await _say()
        await logger.send_log(await _log())
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
    CheckPermission(access_to=0), # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def ban(message: Message, args: Tuple[str]):
    async def _log(UnTime):
        pl = database.get_permission(UserID=About.UserID(message), PeerID=About.PeerID(message))
        text = f"Инициатор: @id{About.UserID(message)} ({await About.UserFullName(message)})\n" \
               f"Роль: {pl} - {PERMISSION_LVL[pl]}\n" \
               f"Источник: {await About.PeerName(message)}\n" \
               f"Команда: /ban \n" \
               f"Цель: @id{About.UserID(message.reply_message)} ({await About.UserFullName(message.reply_message)})\n" \
               f"Время (МСК): {Converter.convert(time.time())}\n" \
               f"Время снятия (МСК): {Converter.convert(UnTime)}\n"

        forward = {
            'peer_id': About.PeerID(message),
            'conversation_message_ids': [About.CvsMessageID(message.reply_message)]
        }

        return {'text': text, 'forward': forward}

    async def _say(UnTime):
        title = f"@id{About.UserID(message.reply_message)} (Пользователь) временно заблокирован.\n" \
                f"Время снятия блокировки: {Converter.convert(UnTime)}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    PeerID = About.PeerID(message)
    UserID = About.UserID(message.reply_message)
    BannedByID = About.UserID(message)

    try:
        BanDeltaTime = (int(args[0]) * TIME_COEFFICENT[args[1]]) if args[0] != 0 \
            else (int(args[0]) + 1 * TIME_COEFFICENT[args[1]])

    except Exception:
        return

    if not database.get_kick(PeerID=PeerID, UserID=UserID):
        UserName = About.UserFullName(message.reply_message)
        UserURL = About.UserURL(message.reply_message)

        BannedByName = About.UserFullName(message)
        BannedByURL = About.UserURL(message)

        BanTime = int(time.time())
        UnbanTime = BanTime + BanDeltaTime

        await _say(UnbanTime)
        await logger.send_log(await _log(UnbanTime))
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
        # TODO: Логи

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
    async def _log(UnTime):
        pl = database.get_permission(UserID=About.UserID(message), PeerID=About.PeerID(message))
        text = f"Инициатор: @id{About.UserID(message)} ({await About.UserFullName(message)})\n" \
               f"Роль: {pl} - {PERMISSION_LVL[pl]}\n" \
               f"Источник: {await About.PeerName(message)}\n" \
               f"Команда: /mute \n" \
               f"Цель: @id{About.UserID(message.reply_message)} ({await About.UserFullName(message.reply_message)})\n" \
               f"Время (МСК): {Converter.convert(time.time())}\n" \
               f"Время снятия (МСК): {Converter.convert(UnTime)}\n"

        forward = {
            'peer_id': About.PeerID(message),
            'conversation_message_ids': [About.CvsMessageID(message.reply_message)]
        }

        return {'text': text, 'forward': forward}

    async def _say(UnTime):
        title = f"@id{About.UserID(message.reply_message)} (Пользователь) временно заглушен.\n" \
                f"Повторная попытка отправить сообщение в чат приведёт к блокировке.\n" \
                f"Время снятия заглушения: {Converter.convert(UnTime)}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    PeerID = About.PeerID(message)
    UserID = About.UserID(message.reply_message)
    MutedByID = About.UserID(message)

    try:
        MuteDeltaTime = (int(args[0]) * TIME_COEFFICENT[args[1]]) if args[0] != 0 \
            else (int(args[0]) + 1 * TIME_COEFFICENT[args[1]])

    except Exception:
        return

    if not database.get_kick(PeerID=PeerID, UserID=UserID):
        UserName = About.UserFullName(message.reply_message)
        UserURL = About.UserURL(message.reply_message)

        MutedByName = About.UserFullName(message)
        MutedByURL = About.UserURL(message)

        MuteTime = int(time.time())
        UnmuteTime = MuteTime + MuteDeltaTime

        await _say(UnmuteTime)
        await logger.send_log(await _log(UnmuteTime))
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
        # TODO: Логи

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
    async def _log(UnTime, WnCount):
        pl = database.get_permission(UserID=About.UserID(message), PeerID=About.PeerID(message))
        text = f"Инициатор: @id{About.UserID(message)} ({await About.UserFullName(message)})\n" \
               f"Роль: {pl} - {PERMISSION_LVL[pl]}\n" \
               f"Источник: {await About.PeerName(message)}\n" \
               f"Команда: /warn \n" \
               f"Цель: @id{About.UserID(message.reply_message)} ({await About.UserFullName(message.reply_message)})\n" \
               f"Количество предупреждений: {WnCount}/3" \
               f"Время (МСК): {Converter.convert(time.time())}\n" \
               f"Время снятия (МСК): {Converter.convert(UnTime)}\n"

        forward = {
            'peer_id': About.PeerID(message),
            'conversation_message_ids': [About.CvsMessageID(message.reply_message)]
        }

        return {'text': text, 'forward': forward}

    async def _say(UnTime, WnCount):
        title = f"@id{About.UserID(message.reply_message)} (Пользователь) получил предупреждение.\n" \
                f"Текущее количество предупреждений: {WnCount}/3.\n" \
                f"Время снятия предупреждений: {Converter.convert(UnTime)}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    PeerID = About.PeerID(message)
    UserID = About.UserID(message.reply_message)
    WarnedByID = About.UserID(message)

    UserName = About.UserFullName(message.reply_message)
    UserURL = About.UserURL(message.reply_message)

    WarnedByName = About.UserFullName(message)
    WarnedByURL = About.UserURL(message)

    WarnTime = int(time.time())
    UnwarnTime = WarnTime + TIME_COEFFICENT["d"]

    WarnCount = database.get_warn(PeerID=PeerID, UserID=UserID) + 1

    await _say(UnwarnTime, WarnCount)
    await logger.send_log(await _log(UnwarnTime, WarnCount))
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
        # TODO: Логи

    pass # TODO: Сделать код

"""
------------------------------------------------------------------------------------------------------------------------
Команда удаляет сообщение(я) пользователя в беседе. 
"""
@bl.chat_message(
    HandleCommand(ALIASES['delete'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=True),
    CheckPermission(access_to=0), # Moderator
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def delete(message: Message):
    async def _log():
        pl = database.get_permission(UserID=About.UserID(message), PeerID=About.PeerID(message))
        text = f"Инициатор: @id{About.UserID(message)} ({await About.UserFullName(message)})\n" \
               f"Роль: {pl} - {PERMISSION_LVL[pl]}\n" \
               f"Источник: {await About.PeerName(message)}\n" \
               f"Команда: /delete \n" \
               f"Время (МСК): {Converter.convert(time.time())}"

        forward = {'peer_id': About.PeerID(message)}
        if message.fwd_messages:
            forward['conversation_message_ids'] = [About.CvsMessageID(m) for m in message.fwd_messages]
        else:
            forward['conversation_message_ids'] = [About.CvsMessageID(message.reply_message)]

        return {'text': text, 'forward': forward}

    async def _collapse(m: Message):
        MessageID = m.conversation_message_id
        PeerID = message.peer_id
        try:
            await bot.api.messages.delete(group_id=GROUP, peer_id=PeerID, cmids=MessageID, delete_for_all=True)

        except Exception:
            ...

    await logger.send_log(await _log())

    if message.fwd_messages:
        for msg in message.fwd_messages:
            await _collapse(msg)

    else:
        await _collapse(message.reply_message)


"""
------------------------------------------------------------------------------------------------------------------------
Команда копирует сообщение пользователя в беседе и отправляет от лица бота. 
"""
@bl.chat_message(
    HandleCommand(ALIASES['copy'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0), # Moderator
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def copy(message: Message):
    async def _log():
        pl = database.get_permission(UserID=About.UserID(message), PeerID=About.PeerID(message))
        text = f"Инициатор: @id{About.UserID(message)} ({await About.UserFullName(message)})\n" \
               f"Роль: {pl} - {PERMISSION_LVL[pl]}\n" \
               f"Источник: {await About.PeerName(message)}\n" \
               f"Команда: /copy\n" \
               f"Время (МСК): {Converter.convert(time.time())}"

        forward = {
            'peer_id': About.PeerID(message),
            'conversation_message_ids': [About.CvsMessageID(message.reply_message)]
        }

        return {'text': text, 'forward': forward}

    await logger.send_log(await _log())
    await message.answer(message.reply_message.text)