from abc import ABC, abstractmethod
from vkbottle import Bot
from config import TOKEN
from database import Processor
from utils import Info
from utils.convertor import Converter


class ABCHandler(ABC):
    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.processor = Processor()
        self.converter = Converter()
        self.info = Info()

    @abstractmethod
    async def check(self):
        pass
