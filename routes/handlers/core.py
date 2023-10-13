"""
File with description of abstract handler.
"""

from vkbottle import Bot
from utils import (
    Informer,
    Converter
)
from routes.processors import CommandProcessor
from config import TOKEN
from data import DataBase

class BaseHandler:
    """
    Template handler class. It is used as a template,
    which contains all the dependencies necessary for executing the checks.
    """

    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.processor = CommandProcessor()
        self.database = DataBase()
        self.converter = Converter()
        self.informer = Informer()
        