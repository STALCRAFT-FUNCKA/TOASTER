from vkbottle.bot import Bot, BotLabeler, Message
from config import TOKEN, GROUP_ID, GROUP_URL, STUFF_ADMIN_ID
from database.sql_interface import Connection
from utils.chat_logger import Logger
from routes.rules.custom_rules import IgnorePermission, HandleIn, OnlyEnrolled
from utils.information_getter import About
from utils.time_converter import Converter

bot = Bot(token=TOKEN)
bl = BotLabeler()
database = Connection('database/database.db')
logger = Logger()
about = About()
converter = Converter()


@bl.chat_message(
    IgnorePermission(ignore_from=1, mode="SELF"),
    HandleIn(handle_log=False, handle_chat=True, send_respond=False),
    OnlyEnrolled(send_respond=False),
    blocking=False
)
async def mutepunish(message: Message):
    async def send_log(data, command):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name"),
            peer_name=data.get("peer_name"),
            command_name=command,
            reason=data.get('reason'),
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
        title = f"@id{data.get('target_id')} (Пользователь) был заблокирован.\n" \
                f"Причина: {data.get('reason')}.\n" \
                f"Время снятия блокировки: {data.get('target_time')}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    async def collapse(m: Message):
        await bot.api.messages.delete(
            group_id=GROUP_ID,
            peer_id=message.peer_id,
            cmids=m.conversation_message_id,
            delete_for_all=True
        )

    if not database.get_mute(peer_id=message.peer_id, user_id=message.from_id):
        return

    else:
        reason = "Нарушение заглушения"
        delta = converter.delta(3, "d")
        all_data = await about.get_all_info(
            cpid=message.peer_id,
            ctid=message.from_id,
            rsn=reason,
            time_delta=delta
        )
        all_data["initiator_id"] = 0
        all_data["initiator_name"] = "Система"
        all_data["initiator_url"] = GROUP_URL
        all_data["chat_id"] = message.peer_id - 2000000000
        all_data["cmids"] = [message.conversation_message_id]

        database.remove_mute(all_data.get('peer_id'), all_data.get('target_id'))
        database.add_ban(all_data)

        await send_respond(all_data)
        await send_log(all_data, command="ban")

        await collapse(message)

        # Исключаем из беседы
        await bot.api.messages.remove_chat_user(all_data.get("chat_id"), all_data.get("target_id"))
