from abc import ABC, abstractmethod
from vkbottle import Bot
from toaster_app.routes.processors import CommandProcessor
from toaster_app.config import TOKEN
from toaster_app.data import DataBase
from toaster_app.utils import Informer, Converter


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
