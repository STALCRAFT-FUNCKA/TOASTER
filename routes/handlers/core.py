"""
File with description of abstract handler.
"""

from abc import (
    ABC,
    abstractmethod
)
from vkbottle import Bot
from utils import (
    Informer,
    Converter
)
from routes.processors import CommandProcessor
from config import TOKEN
from data import DataBase

class ABCHandler(ABC):
    """
    Abstract handler class. It is used as a template,
    which contains all the dependencies necessary for executing the checks.
    """

    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.processor = CommandProcessor()
        self.database = DataBase()
        self.converter = Converter()
        self.informer = Informer()

    @abstractmethod
    async def check(self):
        """
        An abstract method that specifies whether
        something needs to be checked in a handler.
        """

    @abstractmethod
    def egg(self):
        """
        Easert egg. Thank you wr3dmast3r for the good mood.
        """
