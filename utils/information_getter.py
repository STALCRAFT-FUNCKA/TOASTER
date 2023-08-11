import time

from vkbottle.bot import Bot, Message

from config import GROUP_ID, TOKEN, PERMISSION_LVL
from database.interface import Connection
from utils.time_converter import Converter


class About:
    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.database = Connection('database/database.db')
        self.converter = Converter()

    @staticmethod
    def _get_cmids(message: Message):
        return message.conversation_message_id

    @staticmethod
    def _get_user_url(user_id):
        url = f"https://vk.com/id{user_id}"
        return url

    async def _get_user_full_name(self, user_id, tag=False):
        author_info = await self.bot.api.users.get(user_id)
        full_name = f"{author_info[0].first_name} {author_info[0].last_name}"
        if tag:
            full_name = f"@id{user_id} ({full_name})"

        return full_name

    async def _get_peer_name(self, peer_id):
        conversations_info = await self.bot.api.messages.get_conversations_by_id(
            group_id=GROUP_ID,
            peer_ids=peer_id
        )
        return conversations_info.items[0].chat_settings.title

    async def get_all_info(
            self,
            message: Message,
            set_role = 0,
            command = None,
            time_delta = 0,
            destination = None
    ):
        peer_id = message.peer_id
        peer_name = await self._get_peer_name(peer_id)
        peer_destination = destination
        chat_id = message.chat_id
        # -----
        initiator_id = message.from_id
        initiator_name = await self._get_user_full_name(initiator_id)
        initiator_name_tagged = await self._get_user_full_name(initiator_id, tag=True)
        initiator_role = self.database.get_permission(peer_id, initiator_id)
        initiator_url = self._get_user_url(initiator_id)
        # -----
        target_id = message.reply_message.from_id if message.reply_message else None
        target_name = await self._get_user_full_name(target_id) if message.reply_message else None
        target_name_tagged = await self._get_user_full_name(target_id) if message.reply_message else None
        target_url = self._get_user_url(target_id) if message.reply_message else None
        target_set_role = set_role if message.reply_message else None
        target_set_role_name = PERMISSION_LVL.get(set_role) if message.reply_message else None
        target_warns = self.database.get_warn(peer_id, target_id) if message.reply_message else None
        # -----
        command_name = f"{command.__name__}"
        # -----
        now_time_epoch = int(time.time())
        now_time = self.converter.convert(now_time_epoch)
        target_time_epoch = now_time_epoch + time_delta
        target_time = self.converter.convert(target_time_epoch)
        # -----
        if message.fwd_messages:
            cmids = [self._get_cmids(msg) for msg in message.fwd_messages]
        elif message.reply_message:
            cmids = [self._get_cmids(message.reply_message)]
        else:
            cmids = []


        all_data = {
            "peer_id": peer_id,
            "peer_name": peer_name,
            "peer_destination": peer_destination,
            "chat_id": chat_id,
            # -----
            "initiator_id": initiator_id,
            "initiator_name": initiator_name,
            "initiator_name_tagged": initiator_name_tagged,
            "initiator_role": initiator_role,
            "initiator_url": initiator_url,
            # -----
            "target_id": target_id,
            "target_name": target_name,
            "target_name_tagged": target_name_tagged,
            "target_url": target_url,
            "target_set_role": target_set_role,
            "target_set_role_name": target_set_role_name,
            "target_warns": target_warns,
            # -----
            "command_name": command_name,
            # -----
            "now_time_epoch": now_time_epoch,
            "now_time": now_time,
            "target_time_epoch": target_time_epoch,
            "target_time": target_time,
            # -----
            "cmids": cmids
        }

        return all_data