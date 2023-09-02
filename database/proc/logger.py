import json
from typing import Optional
from config import GROUP_ID, TOKEN, PERMISSION_LVL
from vkbottle.bot import Bot
from database.orm import DataBase
from singltone import MetaSingleton
from utils import Converter


class Logger(metaclass=MetaSingleton):
    def _get_log_peers(self):
        res = self.database.conversations.select(
            ("peer_id",),
            peer_type="LOG"
        )
        return [peer_id[0] for peer_id in res]

    def _std_log_data(self):
        self.log_data = {
            'text': None,
            'forward': {},
        }

    def __init__(self):
        self.converter = Converter()
        self.database = DataBase()
        self.bot = Bot(token=TOKEN)

        self.log_data = {}

        self._std_log_data()

    def compose_log_attachments(self, peer_id=None, cmids: Optional[list] = None):
        forward = {
            'peer_id': peer_id,
            'conversation_message_ids': cmids
        }

        self.log_data['forward'] = forward

    def compose_log_data(
            self,
            initiator_name=None,
            initiator_role=None,
            reason=None,
            peer_name=None,
            command_name=None,
            setting_name=None,
            setting_status=None,
            set_role=None,
            target_name=None,
            target_role=None,
            target_warns: int = None,
            now_time: int = None,
            target_time: int = None

    ):
        log_lines = []

        if initiator_name is not None:
            log_lines.append(f"Инициатор: {initiator_name}")
        if initiator_role is not None:
            role_name = PERMISSION_LVL.get(initiator_role, "Неизвестная роль")
            log_lines.append(f"Роль: {initiator_role} - {role_name}")
        if peer_name is not None:
            log_lines.append(f"Источник: {peer_name}")
        if command_name is not None:
            log_lines.append(f"Команда: /{command_name}")
        if setting_name is not None:
            log_lines.append(f"Настройка: {setting_name}")
        if setting_status is not None:
            log_lines.append(f"Значение: {setting_status}")
        if reason is not None:
            log_lines.append(f"Причина: {reason}")
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
            log_lines.append(f"Время (МСК): {self.converter.convert(now_time)}")
        if target_time is not None:
            log_lines.append(f"Время cнятия (МСК): {self.converter.convert(target_time)}")

        self.log_data['text'] = "\n".join(log_lines)

    async def log(self):
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
