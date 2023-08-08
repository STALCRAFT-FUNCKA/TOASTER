from vkbottle.bot import Bot, Message

from Config import GROUP, TOKEN


class About:
    def __init__ (self):
        self.bot = Bot(token = TOKEN)

    @staticmethod
    def UserID(message: Message):
        return message.from_id

    @staticmethod
    def PeerID(message: Message):
        return message.peer_id

    async def UserFirstName(self, message: Message):
        author_info = await self.bot.api.users.get(self.UserID(message))
        return  author_info[0].first_name

    async def UserLastName(self, message: Message):
        author_info = await self.bot.api.users.get(self.UserID(message))
        return author_info[0].last_name

    async def UserFullName(self, message: Message):
        author_info = await self.bot.api.users.get(self.UserID(message))
        return f"{author_info[0].first_name} {author_info[0].last_name}"

    async def PeerName(self, message: Message):
        conversations_info = await self.bot.api.messages.get_conversations_by_id(
            group_id=GROUP,
            peer_ids=self.PeerID(message)
        )
        return conversations_info.items[0].chat_settings.title