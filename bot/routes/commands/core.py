from vkbottle.bot import BotLabeler
from bot.data import InformationProcessor, ReferenceProcessor, CommandProcessor
from bot.utils import *


bl = BotLabeler()

informer = Informer()
converter = Converter()

com_processor = CommandProcessor()
info_processor = InformationProcessor()
ref_processor = ReferenceProcessor()


async def get_cuid(arg):
    screen_name = arg.replace("@", "")
    screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
    uid = await informer.user_id(screen_name=screen_name)
    return uid
