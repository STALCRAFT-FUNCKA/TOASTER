import json
from typing import Optional

from config import GROUP_ID, TOKEN, PERMISSION_LVL, STUFF_ADMIN_ID
from database.interface import Connection

from vkbottle.bot import Bot


class Logger:
    def _get_log_peers(self):
        return self.database.get_conversation(peer_id=-1, destination="LOG")

    def _std_log_data(self):
        self.log_data = {
            'text': None,
            'forward': {},
        }

    def _std_respond_data(self):
        self.respond_data = {
            'text': None,
            'forward': {},
        }

    def __init__(self):
        self.database = Connection('database/database.db')
        self.bot = Bot(token=TOKEN)

        self.log_data = {}
        self.respond_data = {}

        self._std_respond_data()
        self._std_log_data()

    def compose_log_attachments(
            self,
            peer_id=None,
            cmids: Optional[list] = None
    ):

        forward = {
            'peer_id': peer_id,
            'conversation_message_ids': cmids
        }

        self.log_data['forward'] = forward

    def compose_log_data(
            self,
            initiator_name=None,
            initiator_role=None,
            peer_name=None,
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
        if peer_name is not None:
            log_lines.append(f"Источник: {peer_name}")
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

        self.log_data['text'] = "\n".join(log_lines)

    def compose_respond_attachments(
            self,
            peer_id=None,
            cmids: Optional[list] = None
    ):

        forward = {
            'peer_id': peer_id,
            'conversation_message_ids': cmids
        }

        self.respond_data['forward'] = forward

    def compose_respond_data(
            self,
            target_id=None,
            punish_type=None,
            warning_type=None,
            show_stuff=False,
            target_time=None,
            warn_count=None
    ):
        respond_lines = []
        if target_id is not None:
            target_mention = f"@id{target_id} (Пользователь)"
        else:
            target_mention = f"Пользователь"

        if punish_type is not None:
            if punish_type == "KICK":
                respond_lines.append(f"{target_mention} исключён навсегда.")
            elif punish_type == "BAN":
                respond_lines.append(f"{target_mention} временно заблокирован.")
            elif punish_type == "MUTE":
                respond_lines.append(f"{target_mention} временно заглушен.")
            elif punish_type == "WARN":
                respond_lines.append(f"{target_mention} был предупреждён.")
            else:
                respond_lines.append(f"{target_mention} был \"None-type\".")

        if warning_type is not None:
            if warning_type == "KICK":
                ... # Может быть добавлено
            if warning_type == "BAN":
                respond_lines.append("Пользователь будет возвращен в беседу через время.")
            if warning_type == "MUTE":
                respond_lines.append("Повторная попытка отправить сообщение в чат приведёт к блокировке.")
            if warning_type == "WARN":
                respond_lines.append(f"Количество предупреждений: {warn_count}/3")

        if target_time is not None:
            if punish_type == "KICK":
                ... # Может быть добавлено
            elif punish_type == "BAN":
                respond_lines.append(f"Время снятия блокировки: {target_time}")
            elif punish_type == "MUTE":
                respond_lines.append(f"Время снятия заглушения: {target_time}")
            elif punish_type == "WARN":
                respond_lines.append(f"Время снятия предупреждений: {target_time}")
            else:
                respond_lines.append(f"Время снятия: {target_time}")

        if show_stuff:
            respond_lines.append(f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору).")

        self.respond_data['text'] = "\n".join(respond_lines)

    async def respond(self):
        peer_id = self.respond_data.get("peer_id")
        respond_data = self.respond_data

        await self.bot.api.messages.send(
            group_id=GROUP_ID,
            peer_id=peer_id,
            message=respond_data['text'],
            forward=json.dumps(respond_data['forward']),
            random_id=0
        )

        self._std_respond_data()

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
