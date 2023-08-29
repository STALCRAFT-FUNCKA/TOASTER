import time
from abc import ABC, abstractmethod
from vkbottle import Bot
from config import TOKEN
from database.sql_interface import Connection
from utils.chat_logger import Logger
from utils.information_getter import About
from utils.time_converter import Converter


class ABCHandler(ABC):
    async def _send_log(self, peer_id, user_id, command):
        # формируем лог
        self.logger.compose_log_data(
            initiator_name="Система",
            command_name=command,
            peer_name=await self.about.get_peer_name(peer_id),
            target_name=await self.about.get_user_full_name(user_id, tag=True),
            now_time=self.converter.convert(time.time())
        )

        # отправляем лог
        await self.logger.log()

    def __init__(self):
        self.database = Connection('database/database.db')
        self.bot = Bot(token=TOKEN)
        self.logger = Logger()
        self.converter = Converter()
        self.about = About()

    @abstractmethod
    async def check(self):
        pass