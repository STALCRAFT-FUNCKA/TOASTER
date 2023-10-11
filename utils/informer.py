"""
This file contains an informant class.
"""

from vkbottle.bot import Bot
from singltone import MetaSingleton
from config import GROUP_ID, TOKEN
from utils import Converter


class Informer(metaclass=MetaSingleton):
    """
    An informant class, the main functions of which provide 
    the necessary information about objects of the VK platform.
    """

    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.converter = Converter()

    async def user_id(self, screen_name: str):
        """
        Returns the VK user id by his screen name (nickname).

        Args:
            screen_name (str): user display name.

        Returns:
            Union[int, None]: user id.
        """
        info = await self.bot.api.users.get(screen_name)
        if info:
            return info[0].id

        return None

    async def user_name(self, user_id: int, tag=False):
        """
        Finds out the full name of the VK user and returns his First and Last Name. 
        Upon request, his full name can be placed in the VK mentioning structure.

        Args:
            user_id (int): VK user id.
            tag (bool, optional): indicates whether the name is included in the 
            VK mention structure. Defaults to False.

        Returns:
            str: user (tagged) name.
        """
        info = await self.bot.api.users.get(user_id)
        full_name = f"{info[0].first_name} {info[0].last_name}"
        if tag:
            full_name = f"@id{user_id} ({full_name})"

        return full_name

    async def user_pm(self, user_id: int):
        """
        Finds out whether the VK user has personal messages open.

        Args:
            user_id (int): VK user id

        Returns:
            bool: can write private message.
        """
        info = await self.bot.api.users.get(
            user_id,
            fields=["can_write_private_message"]
        )

        if info[0].can_write_private_message == 1:
            return True

        return False

    async def peer_name(self, peer_id: int):
        """
        Recognizes the name of a conversation based on its peer id.

        Args:
            peer_id (int): conversation local id inside bot.

        Returns:
            str: conversation name.
        """
        conversations_info = await self.bot.api.messages.get_conversations_by_id(
            group_id=GROUP_ID,
            peer_ids=peer_id
        )
        return conversations_info.items[0].chat_settings.title
