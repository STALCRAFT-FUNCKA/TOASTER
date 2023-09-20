from abc import ABC, abstractmethod
from vkbottle import Bot
from usr_config import TOKEN
from data import DataBase
from data import CommandProcessor
from utils import Informer
from utils import Converter


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
