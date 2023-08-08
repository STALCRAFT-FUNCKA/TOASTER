from vkbottle import Bot


from config import TOKEN
from database.interface import Connection
from logger.logger import Logger

bot = Bot(token=TOKEN)
database = Connection('database/database.db')
logger = Logger()

class Handler:
    @staticmethod
    def check():
        ...