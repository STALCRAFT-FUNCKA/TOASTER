import json
from typing import Optional

from config import GROUP_ID, TOKEN, PERMISSION_LVL
from database.interface import Connection

from vkbottle.bot import Bot

database = Connection('database/database.db')


class Logger:
    @staticmethod
    def _get_log_peers():
        return database.get_conversation(peer_id=-1, destination="LOG")

    def _std_log_data(self):
        self.log_data = {
            'text': None,
            'forward': {},
        }

    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.log_data = {}

        self._std_log_data()

    def compose_log_attachments(
            self,
            peer_id=None,
            cvs_msg_ids: Optional[list] = None
    ):

        forward = {
            'peer_id': peer_id,
            'conversation_message_ids': cvs_msg_ids
        }

        self.log_data['forward'] = forward

    def compose_log_data(
            self,
            initiator_name=None,
            initiator_role=None,
            source_peer_name=None,
            command_name=None,
            set_role=None,
            target_name=None,
            target_role=None,
            target_warns=None,
            now_time=None,
            target_time=None

    ):
        log_lines = []

        if initiator_name is not None:
            log_lines.append(f"Инициатор: {initiator_name}")
        if initiator_role is not None:
            role_name = PERMISSION_LVL.get(initiator_role, "Неизвестная роль")
            log_lines.append(f"Роль: {initiator_role} - {role_name}")
        if source_peer_name is not None:
            log_lines.append(f"Источник: {source_peer_name}")
        if command_name is not None:
            log_lines.append(f"Команда: /{command_name}")
        if set_role is not None:
            role_name = PERMISSION_LVL.get(set_role, "Неизвестная роль")
            log_lines.append(f"Установленная роль: {set_role} - {role_name}")
        if target_name is not None:
            log_lines.append(f"Цель: {target_name}")
        if target_role is not None:
            role_name = PERMISSION_LVL.get(target_role, "Неизвестная роль")
            log_lines.append(f"Роль цели: {target_role} - {role_name}")
        if target_warns is not None:
            log_lines.append(f"Предупреждения: {target_warns}/3")
        if now_time is not None:
            log_lines.append(f"Время (МСК): {now_time}")
        if target_time is not None:
            log_lines.append(f"Время cнятия (МСК): {target_time}")

        self.log_data['text'] = "\n".join(log_lines),

    async def send(self):
        peers = self._get_log_peers()
        log_data = self.log_data

        for PeerID in peers:
            await self.bot.api.messages.send(
                group_id=GROUP_ID,
                peer_id=PeerID,
                message=log_data['text'],
                forward=json.dumps(log_data['forward']),
                random_id=0
            )

        self._std_log_data()
