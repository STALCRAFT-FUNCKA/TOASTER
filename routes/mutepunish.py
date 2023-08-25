from vkbottle.bot import Bot, BotLabeler, Message
from config import TOKEN, GROUP_ID
from database.sql_interface import Connection
from utils.chat_logger import Logger
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
async def mutepunish(message: Message):
    if not database.get_mute(peer_id=message.peer_id, user_id=message.from_id):
        return

    # TODO:
