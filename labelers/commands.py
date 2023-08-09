from typing import Tuple

from vkbottle.bot import Bot, BotLabeler, Message

from database.interface import Connection
from config import ALIASES, TOKEN, GROUP_ID, SETTINGS, TIME_COEFFICENT, STUFF_ADMIN_ID
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
    async def say_respond(title):
        await message.answer(title)

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=enroll)
    destination = "CHAT"

    # формируем лог
    logger.compose_log_data(
        initiator_name=all_data.get("initiator_name_tagged"),
        initiator_role=all_data.get("initiator_role"),
        peer_name=all_data.get("_get_peer_name"),
        command_name=all_data.get("command_name"),
        now_time=all_data.get("now_time")
    )

    # отправляем лог
    await logger.send()

    # отправляем уведомления в чат
    if database.get_conversation(peer_id=all_data.get("peer_id"),
                                 destination=destination):
        await say_respond("Данные беседы обновлены.")
    else:
        await say_respond(f"Беседа зарегистрирована.")

    # регистрируем беседу в БД
    database.add_conversation(
        peer_id=all_data.get("peer_id"),
        peer_name=all_data.get("_get_peer_name"),
        destination=destination
    )

    # добавляем стандартный набор настроек
    for setting in SETTINGS:
        database.add_setting(
            peer_id=all_data.get("peer_id"),
            setting_name=setting,
            setting_status=SETTINGS[setting]
        )


@bl.chat_message(
    HandleCommand(ALIASES['drop'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Admin
    HandleIn(handle_log=False, handle_chat=True)
)
async def drop(message: Message):
    async def say_respond(title):
        await message.answer(title)

    # получаем предварительные данные
    all_data = await about.get_all_info(message, command=drop)
    destination = "CHAT"

    if database.get_conversation(peer_id=all_data.get("peer_id"), destination=destination):
        # формируем лог
        logger.compose_log_data(
            initiator_name=all_data.get("initiator_name_tagged"),
            initiator_role=all_data.get("initiator_role"),
            peer_name=all_data.get("_get_peer_name"),
            command_name=all_data.get("command_name"),
            now_time=all_data.get("now_time")
        )

        # отправляем лог
        await logger.send()

        # отправляем уведомление в чат
        await say_respond("Регистрация данной беседы упразднена.")

        # удаляем регистрацию беседы из БД
        database.remove_conversation(peer_id=all_data.get("peer_id"))

    else:
        # отправляем уведомление в чат
        await say_respond("Данная беседа не зарегистрирована.")


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
    async def say_respond(title):
        await message.answer(title)

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=enroll_log)
    destination = "LOG"

    # формируем лог
    logger.compose_log_data(
        initiator_name=all_data.get("initiator_name_tagged"),
        initiator_role=all_data.get("initiator_role"),
        peer_name=all_data.get("_get_peer_name"),
        command_name=all_data.get("command_name"),
        now_time=all_data.get("now_time")
    )

    # отправляем лог
    await logger.send()

    # отправляем уведомления в чат
    if database.get_conversation(
            peer_id=all_data.get("peer_id"),
            destination=destination
    ):
        await say_respond("Данные беседы обновлены.")
    else:
        await say_respond(f"Беседа назначена в качестве лог-чата.")

    # регистрируем лог-чат в БД
    database.add_conversation(
        peer_id=all_data.get("peer_id"),
        peer_name=all_data.get("peer_name"),
        destination=destination
    )


@bl.chat_message(
    HandleCommand(ALIASES['drop_log'], ['!', '/'], 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Admin
    HandleIn(handle_log=True, handle_chat=False)
)
async def drop_log(message: Message):
    async def say_respond(title):
        await message.answer(title)

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=drop_log)
    destination = "LOG"

    # проверяем наличие регистрации беседы в БД
    if database.get_conversation(peer_id=all_data.get("peer_id"), destination=destination):
        # формируем лог
        logger.compose_log_data(
            initiator_name=all_data.get("initiator_name_tagged"),
            initiator_role=all_data.get("initiator_role"),
            peer_name=all_data.get("_get_peer_name"),
            command_name=all_data.get("command_name"),
            now_time=all_data.get("now_time")
        )

        # отправляем лог
        await logger.send()

        # отправляем уведомление
        await say_respond("Данный лог-чат упразднён.")

        # удаляем регистрацию лог-чата
        database.remove_conversation(peer_id=all_data.get("peer_id"))

    else:
        # отправляем уведомление
        await say_respond("Беседа не является лог-чатом.")


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
        # получаем все необходимые данные
        all_data = await about.get_all_info(message, command=permission, set_role=int(args[0]))

        # формируем лог
        logger.compose_log_data(
            initiator_name=all_data.get("initiator_name_tagged"),
            initiator_role=all_data.get("initiator_role"),
            peer_name=all_data.get("_get_peer_name"),
            command_name=all_data.get("command_name"),
            set_role=all_data("target_set_role"),
            now_time=all_data.get("now_time")
        )

        # отправляем лог
        await logger.send()

        # добавляем пользователю группу прав
        database.set_permission(
            all_data.get("peer_id"),
            all_data.get("target_id"),
            all_data.get("target_name"),
            all_data.get("target_url"),
            all_data.get("target_set_role"),
            all_data.get("target_set_role_name")
        )

    except Exception as error:
        print("Command aborted: ", error)


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
    async def say_respond():
        title = f"@id{message.reply_message.from_id} (Пользователь) исключен из беседы навсегда.\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=kick)

    # проверяем наличие пользователя в бд
    if not database.get_kick(peer_id=all_data.get("peer_id"), user_id=all_data.get("target_id")):
        # формируем лог
        logger.compose_log_data(
            initiator_name=all_data.get("initiator_name_tagged"),
            initiator_role=all_data.get("initiator_role"),
            peer_name=all_data.get("_get_peer_name"),
            command_name=all_data.get("command_name"),
            now_time=all_data.get("now_time")
        )
        logger.compose_log_attachments(
            peer_id=all_data.get("peer_id"),
            cmids=all_data.get("cmids")
        )

        # отправляем лог
        await logger.send()

        # отправляем уведомление в чат
        await say_respond()

        # Выдаем кик
        database.add_kick(
            all_data.get("peer_id"),
            all_data.get("target_id"),
            all_data.get("target_name"),
            all_data.get("target_url"),
            all_data.get("initiator_id"),
            all_data.get("initiator_name"),
            all_data.get("initiator_url"),
            all_data.get("now_time_epoch")
        )

        # Исключаем из беседы
        await bot.api.messages.remove_chat_user(message.chat_id, all_data.get("target_id"))


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
    async def say_respond(tt):
        title = f"@id{message.reply_message.from_id} (Пользователь) временно заблокирован.\n" \
                f"Время снятия блокировки: {converter.convert(tt)}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    # выводим дельту времени
    try:
        if int(args[0]) > 0:
            delta = (int(args[0]) * TIME_COEFFICENT[args[1]])
        else:
            delta = TIME_COEFFICENT[args[1]]

        # получаем все необходимые данные
        all_data = await about.get_all_info(message, command=ban, time_delta=delta)

        if not database.get_ban(peer_id=all_data.get("peer_id"), user_id=all_data.get("target_id")):
            # формируем лог
            logger.compose_log_data(
                initiator_name=all_data.get("initiator_name_tagged"),
                initiator_role=all_data.get("initiator_role"),
                peer_name=all_data.get("source_peer_name"),
                command_name=all_data.get("command_name"),
                target_warns=all_data.get("warn_count"),
                now_time=all_data.get("now_time"),
                target_time=all_data.get("target_time")
            )
            logger.compose_log_attachments(
                peer_id=all_data.get("peer_id"),
                cmids=all_data.get("cmids")
            )

            # отправляем лог
            await logger.send()

            # отправляем уведомление в чат
            await say_respond(all_data.get("target_time"))

            # выдаем блокировку
            database.add_ban(
                all_data.get("peer_id"),
                all_data.get("target_id"),
                all_data.get("target_name"),
                all_data.get("target_url"),
                all_data.get("initiator_id"),
                all_data.get("initiator_name"),
                all_data.get("initiator_url"),
                all_data.get("now_time_epoch"),
                all_data.get("target_time_epoch")
            )

            # исключаем из беседы
            await bot.api.messages.remove_chat_user(message.chat_id, message.reply_message.from_id)

    except Exception as error:
        print("Command aborted: ", error)


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

    # выводим дельту времени
    try:
        if int(args[0]) > 0:
            delta = (int(args[0]) * TIME_COEFFICENT[args[1]])
        else:
            delta = TIME_COEFFICENT[args[1]]

        # получаем все необходимые данные
        all_data = await about.get_all_info(message, command=mute, time_delta=delta)

        # проверяем наличие пользователя в базе данных
        if not database.get_mute(peer_id=all_data.get("peer_id"), user_id=all_data.get("target_id")):
            # формируем лог
            logger.compose_log_data(
                initiator_name=all_data.get("initiator_name_tagged"),
                initiator_role=all_data.get("initiator_role"),
                peer_name=all_data.get("source_peer_name"),
                command_name=all_data.get("command_name"),
                target_warns=all_data.get("warn_count"),
                now_time=all_data.get("now_time"),
                target_time=all_data.get("target_time")
            )
            logger.compose_log_attachments(
                peer_id=all_data.get("peer_id"),
                cmids=all_data.get("cmids")
            )

            # отправляем лог
            await logger.send()

            # отправляем уведомление в чат
            await say_respond(all_data.get("target_time"))

            # выдаем блокировку
            database.add_mute(
                all_data.get("peer_id"),
                all_data.get("target_id"),
                all_data.get("target_name"),
                all_data.get("target_url"),
                all_data.get("initiator_id"),
                all_data.get("initiator_name"),
                all_data.get("initiator_url"),
                all_data.get("now_time_epoch"),
                all_data.get("target_time_epoch")
            )

    except Exception as error:
        print("Command aborted: ", error)


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
    all_data = await about.get_all_info(message, command=warn)

    # формируем лог
    logger.compose_log_data(
        initiator_name=all_data.get("initiator_name_tagged"),
        initiator_role=all_data.get("initiator_role"),
        peer_name=all_data.get("_get_peer_name"),
        command_name=all_data.get("command_name"),
        target_warns=all_data.get("target_warns"),
        now_time=all_data.get("now_time"),
        target_time=all_data.get("target_time")
    )
    logger.compose_log_attachments(
        peer_id=all_data.get("peer_id"),
        cmids=all_data.get("cmids")
    )

    # отправляем лог
    await logger.send()

    # отправляем уведомление
    await say_respond(
        all_data.get("target_time"),
        all_data.get("target_warns")
    )

    # выдаем предупреждение
    database.add_warn(
        all_data.get("peer_id"),
        all_data.get("target_id"),
        all_data.get("target_name"),
        all_data.get("target_url"),
        all_data.get("initiator_id"),
        all_data.get("initiator_name"),
        all_data.get("initiator_url"),
        all_data.get("now_time_epoch"),
        all_data.get("target_time_epoch"),
        all_data.get("target_warns")
    )

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
        await bot.api.messages.delete(
            group_id=GROUP_ID,
            peer_id=message.peer_id,
            cmids=m.conversation_message_id,
            delete_for_all=True
        )

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=delete)

    # формируем лог
    logger.compose_log_data(
        initiator_name=all_data.get("initiator_name_tagged"),
        initiator_role=all_data.get("initiator_role"),
        peer_name=all_data.get("_get_peer_name"),
        command_name=all_data.get("command_name"),
        now_time=all_data.get("now_time"),
    )
    logger.compose_log_attachments(
        peer_id=all_data.get("peer_id"),
        cmids=all_data.get("cmids")
    )

    try:
        # отправляем лог
        await logger.send()

        # удаляем сообщения
        if message.reply_message:
            await _collapse(message.reply_message)
        else:
            for msg in message.fwd_messages:
                await _collapse(msg)

    except Exception as error:
        print("Command aborted:", error)


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
    all_data = await about.get_all_info(message, command=copy)

    # формируем лог
    logger.compose_log_data(
        initiator_name=all_data.get("initiator_name_tagged"),
        initiator_role=all_data.get("initiator_role"),
        peer_name=all_data.get("_get_peer_name"),
        command_name=all_data.get("command_name"),
        now_time=all_data.get("now_time"),
    )
    logger.compose_log_attachments(
        peer_id=all_data.get("peer_id"),
        cmids=all_data.get("cmids")
    )

    # отправляем лог
    await logger.send()

    # отправляем скопированное сообщение в чат
    await message.answer(message.reply_message.text)
