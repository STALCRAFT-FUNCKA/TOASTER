from typing import Tuple
from vkbottle.bot import Bot, BotLabeler, Message
from database.sql_interface import Connection
from config import ALIASES, TOKEN, STUFF_ADMIN_ID, PREFIXES
from utils import *
from rules import *

bot = Bot(token=TOKEN)
bl = BotLabeler()
database = Connection('database/database.db')
logger = Logger()
about = About()
converter = Converter()

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
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            target_name=data.get("target_name_tagged"),
            command_name=data.get("command_name"),
            now_time=data.get("now_time")
        )
        logger.compose_log_attachments(
            peer_id=data.get("peer_id"),
            cmids=data.get("cmids")
        )

        # отправляем лог
        await logger.log()

    async def send_respond(data):
        title = f"@id{data.get('target_id')} (Пользователь) исключен из всех бесед навсегда.\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await bot.api.messages.send(
            chat_id=all_data.get("chat_id"),
            message=title,
            random_id=0
        )

    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await about.get_user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[0])
    if cuid is None:
        print("Command aborted: Wrong mention")
        return

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=terminate, ctid=cuid)

    for peer_id in database.get_conversation(peer_id=-1, destination="CHAT"):
        all_data["peer_id"] = peer_id
        all_data["chat_id"] = peer_id - 2000000000

        # проверяем наличие пользователя в бд
        if not database.get_kick(all_data.get("peer_id"), all_data.get("target_id")):
            if all_data["peer_name"] != "Все беседы":
                all_data["peer_name"] = "Все беседы"
                # формируем лог
                await send_log(all_data)

            # отправляем уведомление в чат
            await send_respond(all_data)

            # Выдаем кик
            database.add_kick(all_data)

            # Исключаем из беседы
            await bot.api.messages.remove_chat_user(all_data.get("chat_id"), all_data.get("target_id"))


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
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            command_name=data.get("command_name"),
            target_name=data.get("target_name_tagged)"),
            set_role=data.get("target_set_role"),
            now_time=data.get("now_time")
        )

        # отправляем лог
        await logger.log()

    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await about.get_user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[1])
    if cuid is None:
        print("Command aborted: Wrong mention")
        return

    try:
        # получаем все необходимые данные
        all_data = await about.get_all_info(message, command=permission, set_role=int(args[0]), ctid=cuid)

        # вызываем отправку лога
        await send_log(all_data)

        # добавляем пользователю группу прав
        database.set_permission(all_data)

    except Exception as error:
        print("Command aborted: ", error)


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
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            target_name=data.get("target_name_tagged"),
            command_name=data.get("command_name"),
            now_time=data.get("now_time")
        )
        logger.compose_log_attachments(
            peer_id=data.get("peer_id"),
            cmids=data.get("cmids")
        )

        # отправляем лог
        await logger.log()

    async def send_respond(data):
        title = f"@id{data.get('target_id')} (Пользователь) исключен из беседы навсегда.\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await about.get_user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[0])
    if cuid is None:
        print("Command aborted: Wrong mention")
        return

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=kick, ctid=cuid)

    # проверяем наличие пользователя в бд
    if not database.get_kick(all_data.get("peer_id"), all_data.get("target_id")):
        # формируем лог
        await send_log(all_data)

        # отправляем уведомление в чат
        await send_respond(all_data)

        # Выдаем кик
        database.add_kick(all_data)

        # Исключаем из беседы
        await bot.api.messages.remove_chat_user(all_data.get("chat_id"), all_data.get("target_id"))


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
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            command_name=data.get("command_name"),
            target_name=data.get("target_name_tagged"),
            now_time=data.get("now_time"),
            target_time=data.get("target_time")
        )
        logger.compose_log_attachments(
            peer_id=data.get("peer_id"),
            cmids=data.get("cmids")
        )

        # отправляем лог
        await logger.log()

    async def send_respond(data):
        title = f"@id{data.get('target_id')} (Пользователь) временно заблокирован.\n" \
                f"Время снятия блокировки: {data.get('target_time')}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

        # выводим дельту времени

    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await about.get_user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[2])
    if cuid is None:
        print("Command aborted: Wrong mention")
        return

    # получаем дельту времени
    delta = converter.delta(args[0], args[1])

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=ban, time_delta=delta, ctid=cuid)

    if not database.get_ban(all_data.get("peer_id"), all_data.get("target_id")):
        # вызываем отправку лога
        await send_log(all_data)

        # отправляем уведомление в чат
        await send_respond(all_data)

        # выдаем блокировку
        database.add_ban(all_data)

        # исключаем из беседы
        await bot.api.messages.remove_chat_user(all_data.get("chat_id"), all_data.get("target_id"))


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
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            command_name=data.get("command_name"),
            target_name=data.get("target_name_tagged"),
            now_time=data.get("now_time"),
        )

        # отправляем лог
        await logger.log()

    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await about.get_user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[0])
    if cuid is None:
        print("Command aborted: Wrong mention")
        return

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=unban, ctid=cuid)

    if database.get_ban(all_data.get("peer_id"), all_data.get("target_id")):
        # вызываем отправку лога
        await send_log(all_data)

        # снимаем блокировку
        database.remove_ban(all_data.get("peer_id"), all_data.get("target_id"))


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
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            command_name=data.get("command_name"),
            target_name=data.get("target_name_tagged"),
            now_time=data.get("now_time"),
            target_time=data.get("target_time")
        )
        logger.compose_log_attachments(
            peer_id=data.get("peer_id"),
            cmids=data.get("cmids")
        )

        # отправляем лог
        await logger.log()

    async def send_respond(data):
        title = f"@id{data.get('target_id')} (Пользователь) временно заглушен.\n" \
                f"Повторная попытка отправить сообщение в чат приведёт к блокировке.\n" \
                f"Время снятия заглушения: {data.get('target_time')}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await about.get_user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[2])
    if cuid is None:
        print("Command aborted: Wrong mention")
        return

    # выводим дельту времени
    delta = converter.delta(args[0], args[1])

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=mute, time_delta=delta, ctid=cuid)

    # проверяем наличие пользователя в базе данных
    if not database.get_mute(all_data.get("peer_id"), all_data.get("target_id")):
        # вызываем отправку лога
        await send_log(all_data)

        # отправляем уведомление в чат
        await send_respond(all_data)

        # выдаем блокировку
        database.add_mute(all_data)


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
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            command_name=data.get("command_name"),
            target_name=data.get("target_name_tagged"),
            now_time=data.get("now_time"),
            target_time=data.get("target_time")
        )
        logger.compose_log_attachments(
            peer_id=data.get("peer_id"),
            cmids=data.get("cmids")
        )

        # отправляем лог
        await logger.log()

    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await about.get_user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[0])
    if cuid is None:
        print("Command aborted: Wrong mention")
        return

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=unmute, ctid=cuid)

    # проверяем наличие пользователя в базе данных
    if database.get_mute(all_data.get("peer_id"), all_data.get("target_id")):
        # вызываем отправку лога
        await send_log(all_data)

        # выдаем блокировку
        database.remove_mute(all_data.get("peer_id"), all_data.get("target_id"))


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
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            command_name=data.get("command_name"),
            target_name=data.get("target_name_tagged"),
            target_warns=data.get("target_warns"),
            now_time=data.get("now_time"),
            target_time=data.get("target_time")
        )
        logger.compose_log_attachments(
            peer_id=data.get("peer_id"),
            cmids=data.get("cmids")
        )

        # отправляем лог
        await logger.log()

    async def send_respond(data):
        title = f"@id{data.get('target_id')} (Пользователь) получил предупреждение.\n" \
                f"Текущее количество предупреждений: {data.get('target_warns')}/3.\n" \
                f"Время снятия предупреждений: {data.get('target_time')}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await about.get_user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[0])
    if cuid is None:
        print("Command aborted: Wrong mention")
        return

    # выводим дельту времени
    delta = converter.delta(0, "d")

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=warn, time_delta=delta, ctid=cuid)

    # инкриминируем предупреждение
    all_data["target_warns"] += 1

    # вызываем отправку лога
    await send_log(all_data)

    # отправляем уведомление
    await send_respond(all_data)

    # выдаем предупреждение
    database.add_warn(all_data)


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
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            command_name=data.get("command_name"),
            target_name=data.get("target_name_tagged"),
            target_warns=data.get("target_warns"),
            now_time=data.get("now_time")
        )
        logger.compose_log_attachments(
            peer_id=data.get("peer_id"),
            cmids=data.get("cmids")
        )

        # отправляем лог
        await logger.log()

    async def get_cuid(arg):
        screen_name = arg.replace("@", "")
        screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
        uid = await about.get_user_id(screen_name=screen_name)
        return uid

    # Получаем кастомный id пользователя
    cuid = await get_cuid(args[0])
    if cuid is None:
        print("Command aborted: Wrong mention")
        return

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=unwarn, ctid=cuid)

    # инкриминируем предупреждение
    if all_data.get("target_warns") != 0:
        all_data["target_warns"] -= 1

        # вызываем отправку логаы
        await send_log(all_data)

        # выдаем предупреждение
        database.remove_warn(all_data.get("peer_id"), all_data.get("target_id"))
