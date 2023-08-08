from vkbottle import Bot


from config import TOKEN
from DataBase.interface import Connection
from logger.logger import Logger

bot = Bot(token=TOKEN)
database = Connection('DataBase/database.db')
logger = Logger()

class Handler:
    @staticmethod
    def check():
        ...