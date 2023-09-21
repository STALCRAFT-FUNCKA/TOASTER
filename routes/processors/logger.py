import json
from config import PERMISSION_LVL, GROUP_ID, TOKEN
from vkbottle.bot import Bot
from data.orm import DataBase
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

    def compose_log_attachments(self, context):
        if context.get('cmids') is not None:
            forward = {
                'peer_id': context.get('peer_id'),
                'conversation_message_ids': context.get('cmids')
            }

            self.log_data['forward'] = forward

    def compose_log_data(self, context):
        log_lines = []

        if context.get('initiator_nametag') is not None:
            log_lines.append(f"Инициатор: {context.get('initiator_nametag')}")
        if context.get('initiator_lvl') is not None:
            role_name = PERMISSION_LVL.get(context.get('initiator_lvl'), "Неизвестная роль")
            log_lines.append(f"Роль: {context.get('initiator_lvl')} - {role_name}")
        if context.get('peer_name') is not None:
            log_lines.append(f"Источник: {context.get('peer_name')}")
        if context.get('command_name') is not None:
            log_lines.append(f"Команда: /{context.get('command_name') }")
        if context.get('setting_name') is not None:
            log_lines.append(f"Настройка: {context.get('setting_name')}")
        if context.get('setting_status') is not None:
            log_lines.append(f"Значение: {context.get('setting_status')}")
        if context.get('reason') is not None:
            log_lines.append(f"Причина: {context.get('reason')}")
        if context.get('target_lvl') is not None:
            role_name = PERMISSION_LVL.get(context.get('target_lvl'), "Неизвестная роль")
            log_lines.append(f"Установленная роль: {context.get('target_lvl')} - {role_name}")
        if context.get('target_nametag') is not None:
            log_lines.append(f"Цель: {context.get('target_nametag')}")
        if context.get('target_role') is not None:
            role_name = PERMISSION_LVL.get(context.get('target_role'), "Неизвестная роль")
            log_lines.append(f"Роль цели: {context.get('target_role')} - {role_name}")
        if context.get('target_warns') is not None:
            log_lines.append(f"Предупреждения: {context.get('target_warns')}/3")
        if context.get('now_time') is not None:
            log_lines.append(f"Время (МСК): {self.converter.convert(context.get('now_time') )}")
        if context.get('target_time') is not None:
            log_lines.append(f"Время cнятия (МСК): {self.converter.convert(context.get('target_time') )}")

        self.log_data['text'] = "\n".join(log_lines)

    async def log(self, highlighter=False):
        peers = self._get_log_peers()
        log_data = self.log_data
        if highlighter:
            log_data['text'] = "----------------------------------------------\n" + log_data['text']
            log_data['text'] = log_data['text'] + "\n ----------------------------------------------"
        for peer_id in peers:
            await self.bot.api.messages.send(
                group_id=GROUP_ID,
                peer_id=peer_id,
                message=log_data['text'],
                forward=json.dumps(log_data['forward']),
                random_id=0
            )

        self._std_log_data()
