"""
This file contains a description of the processor classes.
A processor is an object that has a certain semantic set of methods
that execute the basic logic of actions inside the bot. In other words,
the logic of filters, commands, handlers, etc.
"""

from singltone import MetaSingleton
from config import PERMISSION_LVL
from .core import StdProcessor


class InformationProcessor(StdProcessor, metaclass=MetaSingleton):
    """
    Implements basic methods that perform specific actions on the command context.
    """

    async def info_permission_proc(self, context):
        """
        Implements the logic of the /info permission command.
        """

        conversations = self.database.conversations.select(
            ("peer_id",)
        )
        conversations = [peer_id[0] for peer_id in conversations]

        for peer_id in conversations:
            peer_name = await self.info.peer_name(peer_id)
            title = f"{peer_name} | Роли: \n"
            text = title

            users = self.database.permissions.select(
                ("target_name", "target_lvl"),
                peer_id=peer_id
            )
            for name, role in users:
                text += f"* {name} -- {role}:{PERMISSION_LVL[role]}\n"

            if text != title:
                await self._send_respond(text, context)

    async def info_setting_proc(self, context):
        """
        Implements the logic of the /info setting command.
        """

        conversations = self.database.conversations.select(
            ("peer_id",),
            peer_type="CHAT"
        )
        conversations = [peer_id[0] for peer_id in conversations]

        for peer_id in conversations:
            peer_name = await self.info.peer_name(peer_id)
            title = f"{peer_name} | Настройки: \n"
            text = title

            settings = self.database.settings.select(
                ("setting_name", "setting_status"),
                peer_id=peer_id
            )
            for name, status in settings:
                text += f"* {name} -- {status}\n"

            if text != title:
                await self._send_respond(text, context)

    async def info_mark_proc(self, context):
        """
        Implements the logic of the /info mark command.
        """

        conversations = self.database.conversations.select(
            ("peer_name", "peer_type")
        )
        title = "Зарегистрированные беседы: \n"
        text = title

        for cname, ctype in conversations:
            text += f"* {cname} -- {ctype} \n"

        if text != title:
            await self._send_respond(text, context)

    async def info_kick_proc(self, context):
        """
        Implements the logic of the /info kick command.
        """

        conversations = self.database.conversations.select(
            ("peer_id",),
            peer_type="CHAT"
        )
        conversations = [peer_id[0] for peer_id in conversations]

        for peer_id in conversations:
            peer_name = await self.info.peer_name(peer_id)
            title = f"{peer_name} | Исключенные пользователи: \n"
            text = title

            kicks = self.database.kicked.select(
                ("initiator_name", "target_name", "kick_time"),
                peer_id=peer_id
            )
            for initiator_name, target_name, kick_time in kicks:
                text += f"* {target_name} -- {self.converter.convert(kick_time)}\n" \
                        f"\\-Инициатор: {initiator_name}\n"

            if text != title:
                await self._send_respond(text, context)

    async def info_ban_proc(self, context):
        """
        Implements the logic of the /info ban command.
        """

        conversations = self.database.conversations.select(
            ("peer_id",),
            peer_type="CHAT"
        )
        conversations = [peer_id[0] for peer_id in conversations]

        for peer_id in conversations:
            peer_name = await self.info.peer_name(peer_id)
            title = f"{peer_name} | Заблокированные пользователи: \n"
            text = title

            bans = self.database.banned.select(
                ("initiator_name", "target_name", "ban_time", "unban_time"),
                peer_id=peer_id
            )
            for initiator_name, target_name, ban_time, unban_time in bans:
                text += f"* {target_name} -- {self.converter.convert(ban_time)}\n" \
                        f"|-Время снятия: {self.converter.convert(unban_time)}\n" \
                        f"\\-Инициатор: {initiator_name}\n"

            if text != title:
                await self._send_respond(text, context)

    async def info_mute_proc(self, context):
        """
        Implements the logic of the /info mute command.
        """

        conversations = self.database.conversations.select(
            ("peer_id",),
            peer_type="CHAT"
        )
        conversations = [peer_id[0] for peer_id in conversations]

        for peer_id in conversations:
            peer_name = await self.info.peer_name(peer_id)
            title = f"{peer_name} | Заглушенные пользователи: \n"
            text = title

            mutes = self.database.muted.select(
                ("initiator_name", "target_name", "mute_time", "unmute_time"),
                peer_id=peer_id
            )
            for initiator_name, target_name, mute_time, unmute_time in mutes:
                text += f"* {target_name} -- {self.converter.convert(mute_time)}\n" \
                        f"|-Время снятия: {self.converter.convert(unmute_time)}\n" \
                        f"\\-Инициатор: {initiator_name}\n"

            if text != title:
                await self._send_respond(text, context)

    async def info_warn_proc(self, context):
        """
        Implements the logic of the /info warn command.
        """

        conversations = self.database.conversations.select(
            ("peer_id",),
            peer_type="CHAT"
        )
        conversations = [peer_id[0] for peer_id in conversations]

        for peer_id in conversations:
            peer_name = await self.info.peer_name(peer_id)
            title = f"{peer_name} | Предупрежденные пользователи: \n"
            text = title

            warns = self.database.warned.select(
                ("initiator_name", "target_name",
                 "warn_time", "unwarn_time", "warn_count"),
                peer_id=peer_id
            )
            for init_name, target_name, warn_time, unwarn_time, warn_count in warns:
                text += f"* {target_name} -- {self.converter.convert(warn_time)}\n" \
                        f"|- Время снятия: {self.converter.convert(unwarn_time)}\n" \
                        f"|- Количество предупреждений: {warn_count}\n" \
                        f"\\- Инициатор: {init_name}\n"

            if text != title:
                await self._send_respond(text, context)
