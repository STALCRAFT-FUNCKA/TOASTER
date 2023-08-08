from vkbottle.bot import Bot, Message

from config import GROUP_ID, TOKEN


class About:
    def __init__(self):
        self.bot = Bot(token=TOKEN)

    @staticmethod
    def get_cmids(message: Message):
        return message.conversation_message_id

    @staticmethod
    async def user_url(user_id):
        return f"https://vk.com/id{user_id}"

    async def user_full_name(self, user_id, tag=False):
        author_info = await self.bot.api.users.get(user_id)
        full_name = f"{author_info[0].first_name} {author_info[0].last_name}"
        if tag:
            full_name = f"@id{user_id} ({full_name})"

        return full_name

    async def peer_name(self, peer_id):
        conversations_info = await self.bot.api.messages.get_conversations_by_id(
            group_id=GROUP_ID,
            peer_ids=peer_id
        )
        return conversations_info.items[0].chat_settings.title
