from abc import ABC, abstractmethod
from vkbottle import Bot
from routes.processors import CommandProcessor
from config import TOKEN
from data import DataBase
from utils import Informer, Converter


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
