from vkbottle import Bot


from Config import TOKEN
from DataBase.Interface import Connection
from Logger.Logger import Logger

bot = Bot(token=TOKEN)
database = Connection('DataBase/database.db')
logger = Logger()

class Handler:
    @staticmethod
    def check():
        ...