"""
This file contains a description of the command processor class.
A processor is an object that has a certain semantic set of methods
that execute the basic logic of actions inside the bot. In other words,
the logic of filters, commands, handlers, etc.
"""


from vkbottle import CodeException
from config import (
    PERMISSION_LVL,
    SETTINGS,
    STAFF_ADMIN_ID,
    GROUP_ID,
)
from singltone import MetaSingleton
from .core import StdProcessor


class CommandProcessor(StdProcessor, metaclass=MetaSingleton):
    """
    Implements basic methods that perform specific actions on the command context.
    """

    # Can't kick\ban\mute\warn user fully (database reject) if True
    __debug = False

    async def chat_proc(self, context, log=True, respond=True):
        """
        Implements the logic of the /mark chat command.
        """

        context["initiator_lvl"] = self._get_initiator_lvl(context)

        is_enrolled = self.database.conversations.select(
            ("peer_id",),
            peer_id=context.get("peer_id"),
            peer_type="CHAT"
        )
        if is_enrolled:
            k = False
            if respond:
                text = "Данные беседы обновлены.\n"
                await self._send_respond(text, context)
        else:
            k = True
            if respond:
                text = "Беседа зарегистрирована.\n"
                await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        self.database.conversations.insert(
            on_duplicate="update",
            peer_id=context.get("peer_id"),
            peer_name=context.get("peer_name"),
            peer_type="CHAT"
        )

        for name, status in SETTINGS.items():
            self.database.settings.insert(
                on_duplicate="ignore",
                peer_id=context.get("peer_id"),
                setting_name=name,
                setting_status=status
            )

        if k:
            self.database.permissions.insert(
                peer_id=context.get("peer_id"),
                target_id=0,
                target_name="Система",
                target_lvl=2
            )

    async def log_proc(self, context: dict, log=True, respond=True):
        """
        Implements the logic of the /mark log command.
        """

        context["initiator_lvl"] = self._get_initiator_lvl(context)

        is_enrolled = self.database.conversations.select(
            ("peer_id",),
            peer_id=context.get("peer_id"),
            peer_type=context.get("peer_type")
        )
        if is_enrolled:
            k = False
            if respond:
                text = "Данные беседы обновлены.\n"
                await self._send_respond(text, context)
        else:
            k = True
            if respond:
                text = "Беседа назначена в качестве лог-чата.\n"
                await self._send_respond(text, context)

        if log:
            await self._send_log(context)

        self.database.conversations.insert(
            on_duplicate="update",
            peer_id=context.get("peer_id"),
            peer_name=context.get("peer_name"),
            peer_type=context.get("peer_type")
        )

        if k:
            self.database.permissions.insert(
                peer_id=context.get("peer_id"),
                target_id=0,
                target_name="Система",
                target_lvl=2
            )

    async def drop_proc(self, context: dict, log=True, respond=True):
        """
        Implements the logic of the /mark drop command.
        """

        is_enrolled = self.database.conversations.select(
            ("peer_id",),
            peer_id=context.get("peer_id"),
        )
        if is_enrolled:
            context["initiator_lvl"] = self._get_initiator_lvl(context)

            if respond:
                text = "Регистрация данной беседы упразднена.\n"
                await self._send_respond(text, context)
            if log:
                await self._send_log(context)

            self.database.conversations.delete(
                peer_id=context.get("peer_id")
            )

        else:
            if respond:
                text = "Данная беседа не зарегистрирована.\n"
                await self._send_respond(text, context)

    async def terminate_proc(
        self, context: dict, collapse=False, log=True, respond=True
    ):
        """
        Implements the logic of the /terminate command.
        """

        context["initiator_lvl"] = self._get_initiator_lvl(context)

        logged = False
        peers = self.database.conversations.select(
            ("peer_id",),
            peer_type="CHAT"
        )
        peers = [peer_id[0] for peer_id in peers]
        for peer_id in peers:
            context["peer_id"] = peer_id
            context["chat_id"] = peer_id - 2000000000

            is_kicked = self.database.kicked.select(
                ("target_name",),
                peer_id=context.get("peer_id"),
                target_id=context.get("target_id")
            )
            if not is_kicked:
                if respond:
                    text = f"@id{context.get('target_id')}"\
                            f" (Пользователь) исключен из всех бесед навсегда.\n"\
                            f"По вопросам обращаться к @id{STAFF_ADMIN_ID}"\
                            f" (Администратору).\n"
                    await self._send_respond(text, context)
                if not logged and log:
                    logged = True
                    await self._send_log(context)

                self.database.kicked.insert(
                    peer_id=context.get("peer_id"),
                    initiator_id=context.get("initiator_id"),
                    initiator_name=context.get("initiator_name"),
                    target_id=context.get("target_id"),
                    target_name=context.get("target_name"),
                    kick_time=context.get("now_time")
                )

                if not self.__debug:
                    await self.bot.api.messages.remove_chat_user(
                        chat_id=context.get("chat_id"),
                        user_id=context.get("target_id")
                    )

        if collapse:
            await self.bot.api.messages.delete(
                group_id=GROUP_ID,
                peer_id=context.get("peer_id"),
                cmids=context.get("cmids"),
                delete_for_all=True
            )

    async def permission_proc(self, context: dict, log=True, respond=True):
        """
        Implements the logic of the /permission command.
        """

        context["initiator_lvl"] = self._get_initiator_lvl(context)

        if respond:
            text = f"@id{context.get('target_id')} (Пользователю) установлена" \
                    f" роль {context.get('target_lvl')}" \
                    f" - {PERMISSION_LVL.get(context.get('target_lvl'))}.\n"
            await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        if context.get("target_lvl") > 0:
            self.database.permissions.insert(
                on_duplicate="update",
                peer_id=context.get("peer_id"),
                target_id=context.get("target_id"),
                target_name=context.get("target_name"),
                target_lvl=context.get("target_lvl")
            )
        else:
            self.database.permissions.delete(
                peer_id=context.get("peer_id"),
                target_id=context.get("target_id"),
            )

    async def kick_proc(self, context: dict, collapse=False, log=True, respond=True):
        """
        Implements the logic of the /kick command.
        """

        is_kicked = self.database.kicked.select(
            ("target_name",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if not is_kicked:
            context["initiator_lvl"] = self._get_initiator_lvl(context)

            if respond:
                rsn = f"Причина: {context.get('reason')} \n"
                text = f"@id{context.get('target_id')} (Пользователь)" \
                        f" исключен из беседы.\n" \
                        f"{rsn if context.get('reason') is not None else ''}" \
                        f"По вопросам обращаться к "\
                        f"@id{STAFF_ADMIN_ID} (Администратору).\n"
                await self._send_respond(text, context)
            if log:
                await self._send_log(context)

            self.database.kicked.insert(
                peer_id=context.get("peer_id"),
                initiator_id=context.get("initiator_id"),
                initiator_name=context.get("initiator_name"),
                target_id=context.get("target_id"),
                target_name=context.get("target_name"),
                kick_time=context.get("now_time")
            )

            if not self.__debug:
                await self.bot.api.messages.remove_chat_user(
                    chat_id=context.get("chat_id"),
                    user_id=context.get("target_id")
                )

        if collapse:
            await self.bot.api.messages.delete(
                group_id=GROUP_ID,
                peer_id=context.get("peer_id"),
                cmids=context.get("cmids"),
                delete_for_all=True
            )

    async def ban_proc(self, context: dict, collapse=False, log=True, respond=True):
        """
        Implements the logic of the /ban command.
        """

        is_banned = self.database.banned.select(
            ("target_name",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if not is_banned:
            context["initiator_lvl"] = self._get_initiator_lvl(context)

            if respond:
                rsn = f"Причина: {context.get('reason')} \n"
                text =  f"@id{context.get('target_id')} (Пользователь) "\
                        f"временно заблокирован.\n" \
                        f"{rsn if context.get('reason') is not None else ''}" \
                        f"Время снятия блокировки: "\
                        f"{self.converter.convert(context.get('target_time'))}\n" \
                        f"По вопросам обращаться к "\
                        f"@id{STAFF_ADMIN_ID} (Администратору).\n"
                await self._send_respond(text, context)
            if log:
                await self._send_log(context)

            self.database.banned.insert(
                peer_id=context.get("peer_id"),
                initiator_id=context.get("initiator_id"),
                initiator_name=context.get("initiator_name"),
                target_id=context.get("target_id"),
                target_name=context.get("target_name"),
                ban_time=context.get("now_time"),
                unban_time=context.get("target_time")
            )

            if not self.__debug:
                await self.bot.api.messages.remove_chat_user(
                    chat_id=context.get("chat_id"),
                    user_id=context.get("target_id")
                )

        if collapse:
            await self.bot.api.messages.delete(
                group_id=GROUP_ID,
                peer_id=context.get("peer_id"),
                cmids=context.get("cmids"),
                delete_for_all=True
            )

    async def unban_proc(self, context: dict, log=True, respond=True):
        """
        Implements the logic of the /unban command.
        """

        is_banned = self.database.banned.select(
            ("target_name",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if is_banned:

            context["initiator_lvl"] = self._get_initiator_lvl(context)

            if respond:
                text = f"@id{context.get('target_id')} (Пользователь) разблокирован.\n"
                await self._send_respond(text, context)
            if log:
                await self._send_log(context)

            self.database.banned.delete(
                peer_id=context.get("peer_id"),
                target_id=context.get("target_id")
            )

    async def mute_proc(self, context: dict, collapse=False, log=True, respond=True):
        """
        Implements the logic of the /mute command.
        """

        is_muted = self.database.muted.select(
            ("target_name",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if not is_muted:
            context["initiator_lvl"] = self._get_initiator_lvl(context)

            if respond:
                rsn = f"Причина: {context.get('reason')} \n"
                text = f"@id{context.get('target_id')} (Пользователь) "\
                        f"временно заглушен.\n" \
                        f"Повторная попытка отправить сообщение в чат "\
                        f"приведёт к блокировке.\n" \
                        f"{rsn if context.get('reason') is not None else ''}" \
                        f"Время снятия заглушения: "\
                        f"{self.converter.convert(context.get('target_time'))}\n" \
                        f"По вопросам обращаться к "\
                        f"@id{STAFF_ADMIN_ID} (Администратору).\n"
                await self._send_respond(text, context)
            if log:
                await self._send_log(context)

            self.database.muted.insert(
                peer_id=context.get("peer_id"),
                initiator_id=context.get("initiator_id"),
                initiator_name=context.get("initiator_name"),
                target_id=context.get("target_id"),
                target_name=context.get("target_name"),
                mute_time=context.get("now_time"),
                unmute_time=context.get("target_time")
            )

        if collapse:
            await self.bot.api.messages.delete(
                group_id=GROUP_ID,
                peer_id=context.get("peer_id"),
                cmids=context.get("cmids"),
                delete_for_all=True
            )

    async def unmute_proc(self, context: dict, log=True, respond=True):
        """
        Implements the logic of the /unmute command.
        """

        is_muted = self.database.muted.select(
            ("target_name",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if is_muted:
            context["initiator_lvl"] = self._get_initiator_lvl(context)

            if respond:
                text = f"@id{context.get('target_id')} (Пользователь) разглушен.\n"
                await self._send_respond(text, context)
            if log:
                await self._send_log(context)

            self.database.muted.delete(
                peer_id=context.get("peer_id"),
                target_id=context.get("target_id")
            )

    async def warn_proc(self, context: dict, collapse=False, log=True, respond=True):
        """
        Implements the logic of the /warn command.
        """

        context["initiator_lvl"] = self._get_initiator_lvl(context)

        warns = self.database.warned.select(
            ("warn_count",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if warns:
            warns = warns[0][0]
        else:
            warns = 0
        context["target_warns"] = warns + 1

        if respond:
            rsn = f"Причина: {context.get('reason')} \n"
            text = f"@id{context.get('target_id')} (Пользователь) "\
                    f"получил предупреждение.\n" \
                    f"{rsn if context.get('reason') is not None else ''}" \
                    f"Текущее количество предупреждений: "\
                    f"{context.get('target_warns')}/3.\n" \
                    f"Время снятия предупреждений: "\
                    f"{self.converter.convert(context.get('target_time'))}\n" \
                    f"По вопросам обращаться к @id{STAFF_ADMIN_ID} (Администратору).\n"
            await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        if context.get("target_warns") == 1:
            self.database.warned.insert(
                peer_id=context.get("peer_id"),
                initiator_id=context.get("initiator_id"),
                initiator_name=context.get("initiator_name"),
                target_id=context.get("target_id"),
                target_name=context.get("target_name"),
                warn_count=context.get("target_warns"),
                warn_time=context.get("now_time"),
                unwarn_time=context.get("target_time")
            )
        else:
            self.database.warned.update(
                {
                    "warn_count": context.get("target_warns"),
                    "warn_time": context.get("now_time"),
                    "unwarn_time": context.get("target_time")
                },
                peer_id=context.get("peer_id"),
                target_id=context.get("target_id")
            )

        if collapse:
            await self.bot.api.messages.delete(
                group_id=GROUP_ID,
                peer_id=context.get("peer_id"),
                cmids=context.get("cmids"),
                delete_for_all=True
            )

    async def unwarn_proc(self, context: dict, force=False, log=True, respond=True):
        """
        Implements the logic of the /unawrn command.
        """

        context["initiator_lvl"] = self._get_initiator_lvl(context)

        warns = self.database.warned.select(
            ("warn_count",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if warns:
            warns = warns[0][0]
        else:
            return

        if not force:
            context["target_warns"] = warns - 1
        else:
            context["target_warns"] = 0

        if respond:
            text = f"С @id{context.get('target_id')} (пользователя) "\
                    f"снято предупреждение.\n"
            await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        # инкриминируем предупреждение
        if context.get("target_warns") != 0 and not force:
            self.database.warned.update(
                {"warn_count": context.get("target_warns")},
                peer_id=context.get("peer_id"),
                target_id=context.get("target_id")
            )
        else:
            self.database.warned.delete(
                peer_id=context.get("peer_id"),
                target_id=context.get("target_id")
            )

    async def copy_proc(self, context: dict, log=True, respond=True):
        """
        Implements the logic of the /copy command.
        """

        context["initiator_lvl"] = self._get_initiator_lvl(context)

        if respond:
            text = "Сообщение скопировано"
            await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        text = context.get("copied") + "\n"
        await self._send_respond(text, context)

    async def delete_proc(self, context: dict, log=True, respond=True):
        """
        Implements the logic of the /delete command.
        """

        context["initiator_lvl"] = self._get_initiator_lvl(context)

        if respond:
            text = "Сообщение(я) удалены.\n"
            await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        try:
            await self.bot.api.messages.delete(
                group_id=GROUP_ID,
                peer_id=context.get("peer_id"),
                cmids=context.get("cmids"),
                delete_for_all=True
            )

        except CodeException[15]:
            return

    async def setting_proc(self, context: dict, log=True, respond=True):
        """
        Implements the logic of the /setting command.
        """

        is_setting = self.database.settings.select(
            ("setting_name",),
            peer_id=context.get("peer_id"),
            setting_name=context.get("setting_name")
        )
        if is_setting:
            context["initiator_lvl"] = self._get_initiator_lvl(context)

            self.database.settings.update(
                {"setting_status": context.get("setting_status")},
                peer_id=context.get("peer_id"),
                setting_name=context.get("setting_name")
            )

            if respond:
                text = f"Настройка {context.get('setting_name')} "\
                        f"для этой беседы изменена на " \
                        f"{context.get('setting_status')}\n"
                await self._send_respond(text, context)
            if log:
                await self._send_log(context)

    async def queue_proc(self, context: dict, log=True, respond=True):
        """
        Implements the logic of the /queue command.
        """

        context["initiator_lvl"] = self._get_initiator_lvl(context)

        if respond:
            text = f"@id{context.get('target_id')} (Пользователь) добавлен в очередь.\n"
            await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        self.database.queue.insert(
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id"),
            target_name=context.get("target_name"),
            send_time=context.get("now_time"),
            next_time=context.get("target_time")
        )

    async def unqueue_proc(self, context: dict, log=True, respond=True):
        """
        Implements the logic of the /unquque command.
        """

        context["initiator_lvl"] = self._get_initiator_lvl(context)

        if respond:
            text = f"@id{context.get('target_id')} (Пользователь) удален из очереди.\n"
            await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        self.database.queue.delete(
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id"),
        )
