import time
from typing import Tuple

from vkbottle.bot import Bot, BotLabeler, Message

from database.interface import Connection
from config import ALIASES, TOKEN, GROUP_ID, SETTINGS, PERMISSION_LVL, TIME_COEFFICENT, STUFF_ADMIN_ID
from logger.logger import Logger
from utils.information_getter import About
from utils.time_converter import Converter
from rules.custom_rules import (
    HandleCommand,
    CollapseCommand,
    AnswerCommand,
    CheckPermission,
    HandleIn,
    OnlyEnrolled,
    IgnorePermission
)

bot = Bot(token=TOKEN)
database = Connection('database/database.db')
logger = Logger()
bl = BotLabeler()

about = About()
converter = Converter()

"""
------------------------------------------------------------------------------------------------------------------------
Команда вывода справки\справочной информации.
"""


@bl.chat_message(
    HandleCommand(ALIASES['reference'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=1),  # Moderator
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
    CheckPermission(access_to=0),  # Admin
    HandleIn(handle_log=False, handle_chat=True)
)
async def enroll(message: Message):
    async def _say(title):
        await message.answer(title)

    # получаем все необходимые данные
    user_id = message.from_id
    peer_id = message.peer_id
    destination = "CHAT"
    initiator_name = await about.user_full_name(user_id, tag=True)
    initiator_role = database.get_permission(peer_id, user_id)
    source_peer_name = await about.peer_name(peer_id)
    now_time = converter.convert(int(time.time()))
    command_name = f"{enroll.__name__}"

    # формируем лог
    logger.compose_log_data(
        initiator_name=initiator_name,
        initiator_role=initiator_role,
        source_peer_name=source_peer_name,
        command_name=command_name,
        now_time=now_time
    )

    # отправляем лог
    await logger.send()

    # отправляем уведомления в чат
    if database.get_conversation(peer_id=peer_id, destination=destination):
        await _say("Данные беседы обновлены.")
    else:
        await _say(f"Беседа зарегистрирована.")

    # регистрируем беседу в БД
    database.add_conversation(peer_id=peer_id, peer_name=source_peer_name, destination=destination)
    # добавляем стандартный набор настроек
    for setting in SETTINGS:
        database.add_setting(peer_id=peer_id, setting_name=setting, setting_status=SETTINGS[setting])


@bl.chat_message(
    HandleCommand(ALIASES['drop'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Admin
    HandleIn(handle_log=False, handle_chat=True)
)
async def drop(message: Message):
    async def _say(title):
        await message.answer(title)

    # получаем предварительные данные
    peer_id = message.peer_id
    destination = "CHAT"

    if database.get_conversation(peer_id=peer_id, destination=destination):
        # получаем все необходимые данные
        user_id = message.from_id
        initiator_name = await about.user_full_name(user_id, tag=True)
        initiator_role = database.get_permission(peer_id, user_id)
        source_peer_name = await about.peer_name(peer_id)
        now_time = converter.convert(int(time.time()))
        command_name = f"{drop.__name__}"

        # формируем лог
        logger.compose_log_data(
            initiator_name=initiator_name,
            initiator_role=initiator_role,
            source_peer_name=source_peer_name,
            command_name=command_name,
            now_time=now_time
        )

        # отправляем лог
        await logger.send()
        # отправляем уведомление в чат
        await _say("Регистрация данной беседы упразднена.")
        # удаляем регистрацию беседы из БД
        database.remove_conversation(peer_id=peer_id)

    else:
        # отправляем уведомление в чат
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
    CheckPermission(access_to=0),  # Admin
    HandleIn(handle_log=True, handle_chat=False)
)
async def enroll_log(message: Message):
    async def _say(title):
        await message.answer(title)

    # получаем все необходимые данные
    user_id = message.from_id
    peer_id = message.peer_id
    destination = "LOG"
    initiator_name = await about.user_full_name(user_id, tag=True)
    initiator_role = database.get_permission(peer_id, user_id)
    source_peer_name = await about.peer_name(peer_id)
    now_time = converter.convert(int(time.time()))
    command_name = f"{enroll_log.__name__}"

    # формируем лог
    logger.compose_log_data(
        initiator_name=initiator_name,
        initiator_role=initiator_role,
        source_peer_name=source_peer_name,
        command_name=command_name,
        now_time=now_time
    )

    # отправляем лог
    await logger.send()

    # отправляем уведомления в чат
    if database.get_conversation(peer_id=peer_id, destination=destination):
        await _say("Данные беседы обновлены.")
    else:
        await _say(f"Беседа назначена в качестве лог-чата.")

    # регистрируем лог-чат в БД
    database.add_conversation(peer_id=peer_id, peer_name=source_peer_name, destination=destination)


@bl.chat_message(
    HandleCommand(ALIASES['drop_log'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Admin
    HandleIn(handle_log=True, handle_chat=False)
)
async def drop_log(message: Message):
    async def _say(title):
        await message.answer(title)

    # получаем предварительные данные
    peer_id = message.peer_id
    destination = "LOG"

    # проверяем наличие регистрации беседы в БД
    if database.get_conversation(peer_id=peer_id, destination=destination):
        # получаем все необходимые данные
        user_id = message.from_id
        initiator_name = await about.user_full_name(user_id, tag=True)
        initiator_role = database.get_permission(peer_id, user_id)
        source_peer_name = await about.peer_name(peer_id)
        now_time = converter.convert(int(time.time()))
        command_name = f"{drop_log.__name__}"

        # формируем лог
        logger.compose_log_data(
            initiator_name=initiator_name,
            initiator_role=initiator_role,
            source_peer_name=source_peer_name,
            command_name=command_name,
            now_time=now_time
        )

        # отправляем лог
        await logger.send()
        # отправляем уведомление
        await _say("Данный лог-чат упразднён.")
        # удаляем регистрацию лог-чата
        database.remove_conversation(peer_id=peer_id)

    else:
        # отправляем уведомление
        await _say("Беседа не является лог-чатом.")


"""
------------------------------------------------------------------------------------------------------------------------
Команда, устанавливающая группу прав пользователю в беседе. 
"""


@bl.chat_message(
    HandleCommand(ALIASES['permission'], ['!', '/'], 1),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0),  # Admin
    HandleIn(handle_log=True, handle_chat=True),
    OnlyEnrolled()
)
async def permission(message: Message, args: Tuple[str]):
    try:
        # выводим число уровня роли
        set_role = int(args[0])
        set_role_name = PERMISSION_LVL[set_role]

        # получаем все необходимые данные
        user_id = message.from_id
        target_user_id = message.reply_message.from_id
        peer_id = message.peer_id
        initiator_name = await about.user_full_name(user_id, tag=True)
        initiator_role = database.get_permission(peer_id, user_id)
        target_name = await about.user_full_name(target_user_id, tag=True)
        target_url = about.user_url(target_user_id)
        source_peer_name = await about.peer_name(peer_id)
        now_time_epoch = int(time.time())
        now_time = converter.convert(now_time_epoch)
        command_name = f"{permission.__name__}"

        # формируем лог
        logger.compose_log_data(
            initiator_name=initiator_name,
            initiator_role=initiator_role,
            source_peer_name=source_peer_name,
            command_name=command_name,
            set_role=set_role,
            now_time=now_time,
        )

        # отправляем лог
        await logger.send()
        # добавляем пользователю группу прав
        database.set_permission(peer_id, user_id, target_name, target_url, set_role, set_role_name)

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
    CheckPermission(access_to=0),  # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def kick(message: Message):
    async def _log():
        pl = database.get_permission(user_id=about.UserID(message), peer_id=about.PeerID(message))
        text = f"Инициатор: @id{about.UserID(message)} ({await about.user_full_name(message)})\n" \
               f"Роль: {pl} - {PERMISSION_LVL[pl]}\n" \
               f"Источник: {await about.peer_name(message)}\n" \
               f"Команда: /kick \n" \
               f"Цель: @id{about.UserID(message.reply_message)} ({await about.user_full_name(message.reply_message)})\n" \
               f"Время (МСК): {converter.convert(time.time())}"

        forward = {
            'peer_id': about.PeerID(message),
            'conversation_message_ids': [about.CvsMessageID(message.reply_message)]
        }

        return {'text': text, 'forward': forward}

    async def _say():
        title = f"@id{about.UserID(message.reply_message)} (Пользователь) исключен из беседы навсегда.\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    PeerID = about.PeerID(message)
    UserID = about.UserID(message.reply_message)
    KickedByID = about.UserID(message)

    if not database.get_kick(peer_id=PeerID, user_id=UserID):
        UserName = about.user_full_name(message.reply_message)
        UserURL = about.user_url(message.reply_message)

        KickedByName = about.user_full_name(message)
        KickedByURL = about.user_url(message)

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
    CheckPermission(access_to=0),  # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def ban(message: Message, args: Tuple[str]):
    async def _log(UnTime):
        pl = database.get_permission(user_id=about.UserID(message), peer_id=about.PeerID(message))
        text = f"Инициатор: @id{about.UserID(message)} ({await about.user_full_name(message)})\n" \
               f"Роль: {pl} - {PERMISSION_LVL[pl]}\n" \
               f"Источник: {await about.peer_name(message)}\n" \
               f"Команда: /ban \n" \
               f"Цель: @id{about.UserID(message.reply_message)} ({await about.user_full_name(message.reply_message)})\n" \
               f"Время (МСК): {converter.convert(time.time())}\n" \
               f"Время снятия (МСК): {converter.convert(UnTime)}\n"

        forward = {
            'peer_id': about.PeerID(message),
            'conversation_message_ids': [about.CvsMessageID(message.reply_message)]
        }

        return {'text': text, 'forward': forward}

    async def _say(UnTime):
        title = f"@id{about.UserID(message.reply_message)} (Пользователь) временно заблокирован.\n" \
                f"Время снятия блокировки: {converter.convert(UnTime)}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    PeerID = about.PeerID(message)
    UserID = about.UserID(message.reply_message)
    BannedByID = about.UserID(message)

    try:
        BanDeltaTime = (int(args[0]) * TIME_COEFFICENT[args[1]]) if args[0] != 0 \
            else (int(args[0]) + 1 * TIME_COEFFICENT[args[1]])

    except Exception:
        return

    if not database.get_kick(peer_id=PeerID, user_id=UserID):
        UserName = about.user_full_name(message.reply_message)
        UserURL = about.user_url(message.reply_message)

        BannedByName = about.user_full_name(message)
        BannedByURL = about.user_url(message)

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
    CheckPermission(access_to=1),  # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unban(message: Message):
    def _log():
        ...
        # TODO: Логи

    pass  # TODO: Сделать код


"""
------------------------------------------------------------------------------------------------------------------------
Команда заглушения пользователя в беседе. 
Временно не позволяет пользователю писать сообщения.
"""


@bl.chat_message(
    HandleCommand(ALIASES['mute'], ['!', '/'], 2),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def mute(message: Message, args: Tuple[str]):
    async def say_respond(tt):
        title = f"@id{message.reply_message.from_id} (Пользователь) временно заглушен.\n" \
                f"Повторная попытка отправить сообщение в чат приведёт к блокировке.\n" \
                f"Время снятия заглушения: {tt}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    # предварительные данные
    user_id = message.from_id
    peer_id = message.peer_id
    target_user_id = message.reply_message.from_id

    # выводим дельту времени
    try:
        delta_time = (int(args[0]) * TIME_COEFFICENT[args[1]]) if args[0] != 0 \
            else (int(args[0]) + 1 * TIME_COEFFICENT[args[1]])
    except Exception:
        return

    # проверяем наличие пользователя в базе данных
    if not database.get_kick(peer_id, target_user_id):
        # получаем все необходимые данные
        initiator_name = await about.user_full_name(user_id, tag=True)
        initiator_role = database.get_permission(peer_id, user_id)
        initiator_url = about.user_url(user_id)
        target_name = await about.user_full_name(target_user_id, tag=True)
        target_url = about.user_url(target_user_id)
        warn_count = database.get_warn(peer_id, target_user_id)
        source_peer_name = await about.peer_name(peer_id)
        now_time_epoch = int(time.time())
        now_time = converter.convert(now_time_epoch)
        target_time_epoch = now_time_epoch + delta_time
        target_time = converter.convert(target_time_epoch)
        command_name = f"{mute.__name__}"

        cvs_msg_ids = [about.get_cmids(message.reply_message)] \
                      or [about.get_cmids(msg) for msg in message.fwd_messages]

        # формируем лог
        logger.compose_log_data(
            initiator_name=initiator_name,
            initiator_role=initiator_role,
            source_peer_name=source_peer_name,
            command_name=command_name,
            target_warns=warn_count,
            now_time=now_time,
            target_time=target_time
        )
        logger.compose_log_attachments(
            peer_id=peer_id,
            cvs_msg_ids=cvs_msg_ids
        )

        # отправляем лог
        await logger.send()

        # отправляем уведомление в чат
        await say_respond(target_time)

        # выдаем заглушение
        database.add_mute(peer_id, target_user_id, target_name, target_url,
                          user_id, initiator_name, initiator_url,
                          now_time_epoch, target_time_epoch)


@bl.chat_message(
    HandleCommand(ALIASES['unmute'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=1),  # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unmute(message: Message):
    def _log():
        ...
        # TODO: Логи

    pass  # TODO: Сделать код


"""
------------------------------------------------------------------------------------------------------------------------
Команда предупреждения пользователя в беседе. 
Выдает пользователю одно временное предупреждение (* из 3).
"""


@bl.chat_message(
    HandleCommand(ALIASES['warn'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def warn(message: Message):
    async def say_respond(tt, wc):
        title = f"@id{message.reply_message.from_id} (Пользователь) получил предупреждение.\n" \
                f"Текущее количество предупреждений: {wc}/3.\n" \
                f"Время снятия предупреждений: {tt}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    # получаем все необходимые данные
    user_id = message.from_id
    target_user_id = message.reply_message.from_id
    peer_id = message.peer_id
    initiator_name = await about.user_full_name(user_id, tag=True)
    initiator_role = database.get_permission(peer_id, user_id)
    initiator_url = about.user_url(user_id)
    target_name = await about.user_full_name(target_user_id, tag=True)
    target_url = about.user_url(target_user_id)
    warn_count = database.get_warn(peer_id, target_user_id) + 1
    source_peer_name = await about.peer_name(peer_id)
    now_time_epoch = int(time.time())
    now_time = converter.convert(now_time_epoch)
    target_time_epoch = now_time_epoch + TIME_COEFFICENT["d"]
    target_time = converter.convert(target_time_epoch)
    command_name = f"{warn.__name__}"

    cvs_msg_ids = [about.get_cmids(message.reply_message)] \
                  or [about.get_cmids(msg) for msg in message.fwd_messages]

    # формируем лог
    logger.compose_log_data(
        initiator_name=initiator_name,
        initiator_role=initiator_role,
        source_peer_name=source_peer_name,
        command_name=command_name,
        target_warns=warn_count,
        now_time=now_time,
        target_time=target_time
    )
    logger.compose_log_attachments(
        peer_id=peer_id,
        cvs_msg_ids=cvs_msg_ids
    )

    # отправляем лог
    await logger.send()

    # отправляем уведомление
    await say_respond(target_time, warn_count)

    # выдаем предупреждение
    database.add_warn(peer_id, target_user_id, target_name, target_url,
                      user_id, initiator_name, initiator_url,
                      now_time_epoch, target_time_epoch, warn_count)
    # TODO: Коротин в бд, разобраться

@bl.chat_message(
    HandleCommand(ALIASES['unwarn'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=1),  # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unwarn(message: Message):
    def _log():
        ...
        # TODO: Логи

    pass  # TODO: Сделать код


"""
------------------------------------------------------------------------------------------------------------------------
Команда удаляет сообщение(я) пользователя в беседе. 
"""


@bl.chat_message(
    HandleCommand(ALIASES['delete'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=True),
    CheckPermission(access_to=0),  # Moderator
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def delete(message: Message):
    async def _collapse(m: Message):
        cmids = m.conversation_message_id
        peer_id = message.peer_id
        try:
            await bot.api.messages.delete(group_id=GROUP_ID, peer_id=peer_id, cmids=cmids, delete_for_all=True)

        except Exception:
            ...

    # получаем все необходимые данные
    user_id = message.from_id
    peer_id = message.peer_id
    initiator_name = await about.user_full_name(user_id, tag=True)
    initiator_role = database.get_permission(peer_id, user_id)
    source_peer_name = await about.peer_name(peer_id)
    now_time = converter.convert(int(time.time()))
    command_name = f"{delete.__name__}"

    cvs_msg_ids = [about.get_cmids(message.reply_message)] \
                  or [about.get_cmids(msg) for msg in message.fwd_messages]
    # TODO: Подшаманить с нонтайпом


    # формируем лог
    logger.compose_log_data(
        initiator_name=initiator_name,
        initiator_role=initiator_role,
        source_peer_name=source_peer_name,
        command_name=command_name,
        now_time=now_time
    )
    logger.compose_log_attachments(
        peer_id=peer_id,
        cvs_msg_ids=cvs_msg_ids
    )

    # отправляем лог
    await logger.send()

    # удаляем сообщения
    await _collapse(message.reply_message)
    for msg in message.fwd_messages:
        await _collapse(msg)


"""
------------------------------------------------------------------------------------------------------------------------
Команда копирует сообщение пользователя в беседе и отправляет от лица бота. 
"""


@bl.chat_message(
    HandleCommand(ALIASES['copy'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def copy(message: Message):
    # получаем все необходимые данные
    user_id = message.from_id
    peer_id = message.peer_id
    initiator_name = await about.user_full_name(user_id, tag=True)
    initiator_role = database.get_permission(peer_id, user_id)
    source_peer_name = await about.peer_name(peer_id)
    now_time = converter.convert(int(time.time()))
    command_name = f"{copy.__name__}"

    cvs_msg_ids = [about.get_cmids(message.reply_message)] \
                  or [about.get_cmids(msg) for msg in message.fwd_messages]

    # формируем лог
    logger.compose_log_data(
        initiator_name=initiator_name,
        initiator_role=initiator_role,
        source_peer_name=source_peer_name,
        command_name=command_name,
        now_time=now_time
    )
    logger.compose_log_attachments(
        peer_id=peer_id,
        cvs_msg_ids=cvs_msg_ids
    )

    # отправляем лог
    await logger.send()

    # отправляем скопированное сообщение в чат
    await message.answer(message.reply_message.text)
