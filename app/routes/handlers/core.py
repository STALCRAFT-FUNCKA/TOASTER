from abc import ABC, abstractmethod
from vkbottle import Bot
from app.usr_config import TOKEN
from app.data import DataBase
from app.data import CommandProcessor
from app.utils import Informer
from app.utils.converter import Converter


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
