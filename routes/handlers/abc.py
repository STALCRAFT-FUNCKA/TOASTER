from abc import ABC, abstractmethod
from vkbottle import Bot
from config import TOKEN
from database.orm import DataBase
from database.proc import CommandProcessor
from utils import Info
from utils.converter import Converter


class ABCHandler(ABC):
    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.database = DataBase()
        self.processor = CommandProcessor()
        self.converter = Converter()
        self.info = Info()

    @abstractmethod
    async def check(self):
        pass
