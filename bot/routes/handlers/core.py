from abc import ABC, abstractmethod
from vkbottle import Bot
from bot.usr_config import TOKEN
from bot.data import DataBase
from bot.data import CommandProcessor
from bot.utils import Informer
from bot.utils.converter import Converter


class ABCHandler(ABC):
    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.database = DataBase()
        self.processor = CommandProcessor()
        self.converter = Converter()
        self.informer = Informer()

    @abstractmethod
    async def check(self):
        pass
