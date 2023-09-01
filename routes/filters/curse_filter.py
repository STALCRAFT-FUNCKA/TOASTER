from vkbottle.bot import Bot, BotLabeler, Message
from config import TOKEN, GROUP_ID, GROUP_URL, CURSE_WORDS
from database.sql_interface import Connection
from routes.rules import IgnorePermission, HandleIn, OnlyEnrolled
from utils import *


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
async def curse(message: Message):

    async def send_log(data, command):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name"),
            peer_name=data.get("peer_name"),
            command_name=command,
            reason=data.get('reason'),
            target_name=data.get("target_name_tagged"),
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

    if database.get_setting(message.peer_id, 'Filter_Curse'):
        for word in CURSE_WORDS:
            if word in message.text:

                all_data = await about.get_all_info(
                    cpid=message.peer_id,
                    ctid=message.from_id,
                    rsn="Нежелательный контент"
                )
                all_data["initiator_id"] = 0
                all_data["initiator_name"] = "Система"
                all_data["initiator_url"] = GROUP_URL
                all_data["chat_id"] = message.peer_id - 2000000000
                all_data["cmids"] = [message.conversation_message_id]

                await collapse(message)
                await send_log(all_data, command="delete")
