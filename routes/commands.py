from typing import Tuple
from vkbottle.bot import Bot, BotLabeler, Message
from database.sql_interface import Connection
from database import Processor
from config import ALIASES, TOKEN, GROUP_ID, SETTINGS, STUFF_ADMIN_ID, PREFIXES
from utils import *
from rules import *

bot = Bot(token=TOKEN)
bl = BotLabeler()
database = Connection('database/database.db')
logger = Logger()
info = About()
converter = Converter()
processor = Processor()

"""
------------------------------------------------------------------------------------------------------------------------
Команда вывода справочной информации.
"""


@bl.chat_message(
    HandleCommand(ALIASES['reference'], PREFIXES, 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=1),  # Moderator
    HandleIn(handle_log=True, handle_chat=False)
)
async def reference(message: Message):
    async def send_respond(title):
        await message.answer(title)

    url = "https://github.com/Oidaho/FUNCKA-BOT/blob/master/README.md"
    await send_respond(f"Перейдя по этой ссылке, вы сможете найти документацию на GitHub:\n {url}")


"""
------------------------------------------------------------------------------------------------------------------------
Команда регистрации беседы. 
Бот не будет производить никаких действий в беседе, пока она не будет зарегистрирована.
"""


@bl.chat_message(
    HandleCommand(ALIASES['enroll'], PREFIXES, 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Admin
    HandleIn(handle_log=False, handle_chat=True)
)
async def enroll(message: Message):
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            command_name=data.get("command_name"),
            now_time=data.get("now_time")
        )

        # отправляем лог
        await logger.log()

    async def send_respond(title):
        await message.answer(title)

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=enroll, destination="CHAT")

    # отправляем уведомления в чат
    if database.get_conversation(all_data.get("peer_id"), destination="CHAT"):
        k = False
        await send_respond("Данные беседы обновлены.")
    else:
        k = True
        await send_respond(f"Беседа зарегистрирована.")

    # регистрируем беседу в БД
    database.add_conversation(all_data)

    if k:
        for stng in SETTINGS:
            database.add_setting(data=all_data, setting_name=stng, setting_status=SETTINGS[stng])

    # вызываем отправку лога
    await send_log(all_data)


@bl.chat_message(
    HandleCommand(ALIASES['drop'], PREFIXES, 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Admin
    HandleIn(handle_log=False, handle_chat=True)
)
async def drop(message: Message):
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            command_name=data.get("command_name"),
            now_time=data.get("now_time")
        )

        # отправляем лог
        await logger.log()

    async def send_respond(title):
        await message.answer(title)

    # получаем предварительные данные
    all_data = await about.get_all_info(message, command=drop, destination="CHAT")

    if database.get_conversation(all_data.get("peer_id"), destination="CHAT"):
        # вызываем отправку лога
        await send_log(all_data)

        # отправляем уведомление в чат
        await send_respond("Регистрация данной беседы упразднена.")

        # удаляем регистрацию беседы из БД
        database.remove_conversation(all_data.get("peer_id"))

    else:
        # отправляем уведомление в чат
        await send_respond("Данная беседа не зарегистрирована.")


"""
------------------------------------------------------------------------------------------------------------------------
Команда регистрации лог-чата. 
Таких лог-чатов может быть несколько.
Бот отправляет логи своих действий в каждый из помеченных этой командой чатов.
"""


@bl.chat_message(
    HandleCommand(ALIASES['enroll_log'], PREFIXES, 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Admin
    HandleIn(handle_log=True, handle_chat=False)
)
async def enroll_log(message: Message):
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            command_name=data.get("command_name"),
            now_time=data.get("now_time")
        )

        # отправляем лог
        await logger.log()

    async def send_respond(title):
        await message.answer(title)

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=enroll_log, destination="LOG")

    # регистрируем лог-чат в БД
    database.add_conversation(all_data)

    # отправляем уведомления в чат
    if database.get_conversation(all_data.get("peer_id"), destination="LOG"):
        await send_respond("Данные беседы обновлены.")
    else:
        await send_respond(f"Беседа назначена в качестве лог-чата.")

    # вызываем отправку лога
    await send_log(all_data)


@bl.chat_message(
    HandleCommand(ALIASES['drop_log'], PREFIXES, 0),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Admin
    HandleIn(handle_log=True, handle_chat=False)
)
async def drop_log(message: Message):
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            command_name=data.get("command_name"),
            now_time=data.get("now_time")
        )

        # отправляем лог
        await logger.log()

    async def send_respond(title):
        await message.answer(title)

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=drop_log, destination="LOG")

    # проверяем наличие регистрации беседы в БД
    if database.get_conversation(all_data.get("peer_id"), destination="LOG"):
        # отправляем уведомление
        await send_respond("Данный лог-чат упразднён.")

        # удаляем регистрацию лог-чата
        database.remove_conversation(all_data)

        # вызываем отправку лога
        await send_log(all_data)

    else:
        # отправляем уведомление
        await send_respond("Беседа не является лог-чатом.")


"""
------------------------------------------------------------------------------------------------------------------------
Команда, устанавливающая группу прав пользователю в беседе. 
"""


@bl.chat_message(
    HandleCommand(ALIASES['permission'], PREFIXES, 1),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0),  # Admin
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

    try:
        # получаем все необходимые данные
        all_data = await about.get_all_info(message, command=permission, set_role=int(args[0]))

        # вызываем отправку лога
        await send_log(all_data)

        # добавляем пользователю группу прав
        database.set_permission(all_data)

    except Exception as error:
        print("Command aborted: ", error)


"""
------------------------------------------------------------------------------------------------------------------------
Команда кика пользователя со ВСЕХ бесед. 
Бессрочно исключает пользователя из  ВСЕХ бесед.
"""


@bl.chat_message(
    HandleCommand(ALIASES['terminate'], PREFIXES, 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0),  # Administrator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def terminate(message: Message):
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

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=terminate)

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
Команда кика пользователя с беседы. 
Бессрочно исключает пользователя из беседы.
"""


@bl.chat_message(
    HandleCommand(ALIASES['kick'], PREFIXES, 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def kick(message: Message):
    # получаем все необходимые данные
    context = {
        "peer_id": message.peer_id,
        "peer_name": info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": info.user_name(message.from_id, tag=False),
        "initiator_nametag": info.user_name(message.from_id, tag=True),
        "target_id": message.reply_message.from_id,
        "target_name": info.user_name(message.reply_message.from_id, tag=False),
        "target_nametag": info.user_name(message.reply_message.from_id, tag=True),
        "command_name": "kick",
        "now_time": converter.now(),
        "cmids": [message.conversation_message_id]
    }

    await processor.kick_proc(context, log=True, respond=True)


"""
------------------------------------------------------------------------------------------------------------------------
Команда блокировки пользователя в беседе. 
Временно исключает пользователя из беседы.
"""


@bl.chat_message(
    HandleCommand(ALIASES['ban'], PREFIXES, 2),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def ban(message: Message, args: Tuple[str]):
    try:
        time = int(args[0])
        coefficent = args[1]
    except Exception as error:
        print("Wrong args format. Setting default punish time: ", error)
        time = 1
        coefficent = "h"

    # получаем все необходимые данные
    context = {
        "peer_id": message.peer_id,
        "peer_name": info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": info.user_name(message.from_id, tag=False),
        "initiator_nametag": info.user_name(message.from_id, tag=True),
        "target_id": message.reply_message.from_id,
        "target_name": info.user_name(message.reply_message.from_id, tag=False),
        "target_nametag": info.user_name(message.reply_message.from_id, tag=True),
        "command_name": "ban",
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficent),
        "cmids": [message.conversation_message_id]
    }

    await processor.ban_proc(context, log=True, respond=True)


@bl.chat_message(
    HandleCommand(ALIASES['unban'], PREFIXES, 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unban(message: Message):
    context = {
        "peer_id": message.peer_id,
        "peer_name": info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": info.user_name(message.from_id, tag=False),
        "initiator_nametag": info.user_name(message.from_id, tag=True),
        "target_id": message.reply_message.from_id,
        "target_name": info.user_name(message.reply_message.from_id, tag=False),
        "target_nametag": info.user_name(message.reply_message.from_id, tag=True),
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
    HandleCommand(ALIASES['mute'], PREFIXES, 2),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def mute(message: Message, args: Tuple[str]):
    try:
        time = int(args[0])
        coefficent = args[1]
    except Exception as error:
        print("Wrong args format. Setting default punish time: ", error)
        time = 1
        coefficent = "h"

    # получаем все необходимые данные
    context = {
        "peer_id": message.peer_id,
        "peer_name": info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": info.user_name(message.from_id, tag=False),
        "initiator_nametag": info.user_name(message.from_id, tag=True),
        "target_id": message.reply_message.from_id,
        "target_name": info.user_name(message.reply_message.from_id, tag=False),
        "target_nametag": info.user_name(message.reply_message.from_id, tag=True),
        "command_name": "mute",
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficent),
        "cmids": [message.conversation_message_id]
    }

    await processor.mute_proc(context, log=True, respond=True)


@bl.chat_message(
    HandleCommand(ALIASES['unmute'], PREFIXES, 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=1),  # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unmute(message: Message):
    context = {
        "peer_id": message.peer_id,
        "peer_name": info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": info.user_name(message.from_id, tag=False),
        "initiator_nametag": info.user_name(message.from_id, tag=True),
        "target_id": message.reply_message.from_id,
        "target_name": info.user_name(message.reply_message.from_id, tag=False),
        "target_nametag": info.user_name(message.reply_message.from_id, tag=True),
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
    HandleCommand(ALIASES['warn'], PREFIXES, 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    IgnorePermission(ignore_from=1, mode="TARGET"),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def warn(message: Message):
    time = 1
    coefficent = "d"

    context = {
        "peer_id": message.peer_id,
        "peer_name": info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": info.user_name(message.from_id, tag=False),
        "initiator_nametag": info.user_name(message.from_id, tag=True),
        "target_id": message.reply_message.from_id,
        "target_name": info.user_name(message.reply_message.from_id, tag=False),
        "target_nametag": info.user_name(message.reply_message.from_id, tag=True),
        "command_name": "warn",
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficent),
        "cmids": [message.conversation_message_id]
    }

    await processor.warn_proc(context, log=True, respond=True)


@bl.chat_message(
    HandleCommand(ALIASES['unwarn'], PREFIXES, 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def unwarn(message: Message):
    context = {
        "peer_id": message.peer_id,
        "peer_name": info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": info.user_name(message.from_id, tag=False),
        "initiator_nametag": info.user_name(message.from_id, tag=True),
        "target_id": message.reply_message.from_id,
        "target_name": info.user_name(message.reply_message.from_id, tag=False),
        "target_nametag": info.user_name(message.reply_message.from_id, tag=True),
        "command_name": "unwarn",
        "now_time": converter.now(),
        "cmids": [message.conversation_message_id]
    }

    await processor.unwarn_proc(context, log=True, respond=True)

"""
------------------------------------------------------------------------------------------------------------------------
Команда удаляет сообщение(я) пользователя в беседе. 
"""


@bl.chat_message(
    HandleCommand(ALIASES['delete'], PREFIXES, 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=True),
    CheckPermission(access_to=0),  # Moderator
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def delete(message: Message):
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            command_name=data.get("command_name"),
            now_time=data.get("now_time"),
        )
        logger.compose_log_attachments(
            peer_id=data.get("peer_id"),
            cmids=data.get("cmids")
        )

        # отправляем лог
        await logger.log()

    async def collapse(m: Message):
        await bot.api.messages.delete(
            group_id=GROUP_ID,
            peer_id=message.peer_id,
            cmids=m.conversation_message_id,
            delete_for_all=True
        )

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=delete)

    try:
        # вызываем отправку лога
        await send_log(all_data)

        # удаляем сообщения
        if message.reply_message:
            await collapse(message.reply_message)
        else:
            for msg in message.fwd_messages:
                await collapse(msg)

    except Exception as error:
        print("Command aborted:", error)


"""
------------------------------------------------------------------------------------------------------------------------
Команда копирует сообщение пользователя в беседе и отправляет от лица бота. 
"""


@bl.chat_message(
    HandleCommand(ALIASES['copy'], PREFIXES, 0),
    CollapseCommand(),
    AnswerCommand(use_reply=True, use_fwd=False),
    CheckPermission(access_to=0),  # Moderator
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def copy(message: Message):
    async def send_log(data):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            command_name=data.get("command_name"),
            now_time=data.get("now_time"),
        )
        logger.compose_log_attachments(
            peer_id=data.get("peer_id"),
            cmids=data.get("cmids")
        )

        # отправляем лог
        await logger.log()

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=copy)

    # вызываем отправку лога
    await send_log(all_data)

    # отправляем скопированное сообщение в чат
    await message.answer(message.reply_message.text)


"""
------------------------------------------------------------------------------------------------------------------------
Команда изменяет значение настроек в беседе. 
"""


@bl.chat_message(
    HandleCommand(ALIASES['setting'], PREFIXES, 2),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=0),  # Admin
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def setting(message: Message, args: Tuple):
    async def send_log(data, stgn, stts):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name_tagged"),
            initiator_role=data.get("initiator_role"),
            peer_name=data.get("peer_name"),
            command_name=data.get("command_name"),
            setting_name=stgn,
            setting_status=stts,
            now_time=data.get("now_time"),
        )

        # отправляем лог
        await logger.log()

    async def send_respond(stgn, stts):
        title = f"Настройка {stgn} для этой беседы изменена на {stts}\n"
        await message.answer(title)

    setting_name = args[0]
    setting_status = args[1]

    # получаем все необходимые данные
    all_data = await about.get_all_info(message, command=setting)

    if database.get_setting(peer_id=all_data.get("peer_id"), setting_name=setting_name) is not None:
        database.add_setting(all_data, setting_status=setting_status, setting_name=setting_name)

        await send_respond(setting_name, setting_status)
        await send_log(all_data, setting_name, setting_status)
