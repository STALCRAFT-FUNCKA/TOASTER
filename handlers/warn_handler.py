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

    # TODO: Сделать проверку на кол-во варнов. Если 3 варна - выдать мут.
    # TODO: Сделать проверку на время варна. Если время варна истекло - полностью снять все варны.