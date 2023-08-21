from vkbottle.bot import Bot, BotLabeler, Message
from config import TOKEN, GROUP_ID
from database.interface import Connection
from logger.logger import Logger
from rules.custom_rules import IgnorePermission, HandleIn
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
    blocking=False
)
async def queue(message: Message):
    async def collapse(m: Message):
        await bot.api.messages.delete(
            group_id=GROUP_ID,
            peer_id=message.peer_id,
            cmids=m.conversation_message_id,
            delete_for_all=True
        )

    if not database.get_setting(peer_id=message.peer_id, setting_name="Slow_Mode"):
        return

    else:
        all_data = await about.get_all_info(message)

    if database.get_queue(peer_id=all_data.get("peer_id"), user_id=all_data.get("initiator_id")):
        reason = "Нарушение задержки"
        ...
        # warn

        await collapse(message)

    else:
        database.add_queue(all_data)



