from vkbottle.bot import Bot
from bot.singltone import MetaSingleton
from bot.usr_config import GROUP_ID, TOKEN
from bot.utils.converter import Converter


class Informer(metaclass=MetaSingleton):
    def __init__(self):
        self.bot = Bot(token=TOKEN)

        self.converter = Converter()

    async def user_id(self, screen_name):
        info = await self.bot.api.users.get(screen_name)
        if info:
            return info[0].id
        else:
            return None

    async def user_name(self, user_id, tag=False):
        info = await self.bot.api.users.get(user_id)
        full_name = f"{info[0].first_name} {info[0].last_name}"
        if tag:
            full_name = f"@id{user_id} ({full_name})"

        return full_name

    async def peer_name(self, peer_id):
        conversations_info = await self.bot.api.messages.get_conversations_by_id(
            group_id=GROUP_ID,
            peer_ids=peer_id
        )
        return conversations_info.items[0].chat_settings.title
