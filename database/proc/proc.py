from vkbottle import Bot
from config import TOKEN, STUFF_ADMIN_ID, PERMISSION_LVL, GROUP_ID, SETTINGS
from database.orm import DataBase
from database.proc.logger import Logger
from singltone import MetaSingleton
from utils import Converter, Info


class StdProcessor:
    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.database = DataBase()
        self.logger = Logger()
        self.info = Info()
        self.converter = Converter()


class CommandProcessor(StdProcessor, metaclass=MetaSingleton):
    __debug = False

    async def chat_proc(self, context, log=True, respond=True):
        async def send_log(ctx):
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason"),
                now_time=ctx.get("now_time")
            )

            await self.logger.log()

        async def send_respond(ctx, text):
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        role = self.database.permissions.select(
            ("target_lvl",),
            peer_id=context.get("peer_id"),
            target_id=context.get("initiator_id")
        )
        if role:
            role = role[0][0]
        else:
            role = 0
        context["initiator_lvl"] = role

        is_enrolled = self.database.conversations.select(
            ("peer_id",),
            peer_id=context.get("peer_id"),
            peer_type="CHAT"
        )
        if is_enrolled:
            k = False
            if respond:
                await send_respond(context, "Данные беседы обновлены.")
        else:
            k = True
            if respond:
                await send_respond(context, "Беседа зарегистрирована.")
        if log:
            await send_log(context)

        self.database.conversations.insert(
            peer_id=context.get("peer_id"),
            peer_name=context.get("peer_name"),
            peer_type="CHAT"
        )

        if k:
            for name, status in SETTINGS.items():
                print(name, status)
                self.database.settings.insert(
                    peer_id=context.get("peer_id"),
                    setting_name=name,
                    setting_status=status
                )

    async def log_proc(self, context: dict, log=True, respond=True):
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                now_time=ctx.get("now_time")
            )

            await self.logger.log()

        async def send_respond(ctx, text):
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        role = self.database.permissions.select(
            ("target_lvl",),
            peer_id=context.get("peer_id"),
            target_id=context.get("initiator_id")
        )
        if role:
            role = role[0][0]
        else:
            role = 0
        context["initiator_lvl"] = role

        if respond:
            is_enrolled = self.database.conversations.select(
                ("peer_id",),
                peer_id=context.get("peer_id"),
                peer_type=context.get("peer_type")
            )
            if is_enrolled:
                await send_respond(context, "Данные беседы обновлены.")
            else:
                await send_respond(context, "Беседа назначена в качестве лог-чата.")
        if log:
            await send_log(context)

        self.database.conversations.insert(
            peer_id=context.get("peer_id"),
            peer_name=context.get("peer_name"),
            peer_type=context.get("peer_type")
        )

    async def drop_proc(self, context: dict, log=True, respond=True):
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                now_time=ctx.get("now_time")
            )

            await self.logger.log()

        async def send_respond(ctx, text):
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        is_enrolled = self.database.conversations.select(
            ("peer_id",),
            peer_id=context.get("peer_id"),
        )
        if is_enrolled:
            role = self.database.permissions.select(
                ("target_lvl",),
                peer_id=context.get("peer_id"),
                target_id=context.get("initiator_id")
            )
            if role:
                role = role[0][0]
            else:
                role = 0
            context["initiator_lvl"] = role

            if respond:
                await send_respond(context, "Регистрация данной беседы упразднена.")
            if log:
                await send_log(context)

            self.database.conversations.delete(
                peer_id=context.get("peer_id")
            )

        else:
            if respond:
                await send_respond(context, "Данная беседа не зарегистрирована.")

    async def terminate_proc(self, context: dict, collapse=False, log=True, respond=True):
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                target_name=ctx.get("target_nametag"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                now_time=ctx.get("now_time")
            )
            self.logger.compose_log_attachments(
                peer_id=ctx.get("peer_id"),
                cmids=ctx.get("cmids")
            )

            # отправляем лог
            await self.logger.log()

        async def send_respond(ctx):
            title = f"@id{ctx.get('target_id')} (Пользователь) исключен из всех бесед навсегда.\n" \
                    f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=title,
                random_id=0
            )

        role = self.database.permissions.select(
            ("target_lvl",),
            peer_id=context.get("peer_id"),
            target_id=context.get("initiator_id")
        )
        if role:
            role = role[0][0]
        else:
            role = 0
        context["initiator_lvl"] = role

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
                if not logged and log:
                    logged = True
                    await send_log(context)
                if respond:
                    await send_respond(context)

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
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                target_name=ctx.get("target_nametag"),
                set_role=ctx.get("target_lvl"),
                now_time=ctx.get("now_time")
            )

            # отправляем лог
            await self.logger.log()

        async def send_respond(ctx):
            text = f"@id{ctx.get('target_id')} (Пользователю) установлена роль {context.get('target_lvl')}" \
                   f" - {PERMISSION_LVL.get(context.get('target_lvl'))}.\n"
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        role = self.database.permissions.select(
            ("target_lvl",),
            peer_id=context.get("peer_id"),
            target_id=context.get("initiator_id")
        )
        if role:
            role = role[0][0]
        else:
            role = 0
        context["initiator_lvl"] = role

        if respond:
            await send_respond(context)
        if log:
            await send_log(context)

        if context.get("target_lvl") > 0:
            self.database.permissions.insert(
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
        async def send_log(ctx):
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                target_name=ctx.get("target_nametag"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                now_time=ctx.get("now_time")
            )
            self.logger.compose_log_attachments(
                peer_id=ctx.get("peer_id"),
                cmids=ctx.get("cmids")
            )

            await self.logger.log()

        async def send_respond(ctx):
            rsn = f"Причина: {ctx.get('reason')} \n"
            text = f"@id{ctx.get('target_id')} (Пользователь) исключен из беседы.\n" \
                   f"{rsn if ctx.get('reason') is not None else ''}" \
                   f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        is_kicked = self.database.kicked.select(
            ("target_name",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if not is_kicked:
            role = self.database.permissions.select(
                ("target_lvl",),
                peer_id=context.get("peer_id"),
                target_id=context.get("initiator_id")
            )
            if role:
                role = role[0][0]
            else:
                role = 0
            context["initiator_lvl"] = role

            if respond:
                await send_respond(context)
            if log:
                await send_log(context)

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
        async def send_log(ctx):
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                target_name=ctx.get("target_nametag"),
                now_time=ctx.get("now_time"),
                target_time=ctx.get("target_time")
            )
            self.logger.compose_log_attachments(
                peer_id=ctx.get("peer_id"),
                cmids=ctx.get("cmids")
            )

            await self.logger.log()

        async def send_respond(ctx):
            rsn = f"Причина: {ctx.get('reason')} \n"
            text = f"@id{ctx.get('target_id')} (Пользователь) временно заблокирован.\n" \
                   f"{rsn if ctx.get('reason') is not None else ''}" \
                   f"Время снятия блокировки: {self.converter.convert(ctx.get('target_time'))}\n" \
                   f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        is_banned = self.database.banned.select(
            ("target_name",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if not is_banned:
            role = self.database.permissions.select(
                ("target_lvl",),
                peer_id=context.get("peer_id"),
                target_id=context.get("initiator_id")
            )
            if role:
                role = role[0][0]
            else:
                role = 0
            context["initiator_lvl"] = role

            if respond:
                await send_respond(context)
            if log:
                await send_log(context)

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
        async def send_log(ctx):
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                target_name=ctx.get("target_nametag"),
                now_time=ctx.get("now_time"),
            )

            await self.logger.log()

        async def send_respond(ctx):
            text = f"@id{ctx.get('target_id')} (Пользователь) разблокирован.\n"
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        is_banned = self.database.banned.select(
            ("target_name",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if is_banned:
            role = self.database.permissions.select(
                ("target_lvl",),
                peer_id=context.get("peer_id"),
                target_id=context.get("initiator_id")
            )
            if role:
                role = role[0][0]
            else:
                role = 0
            context["initiator_lvl"] = role

            if respond:
                await send_respond(context)
            if log:
                await send_log(context)

            self.database.banned.delete(
                peer_id=context.get("peer_id"),
                target_id=context.get("target_id")
            )

    async def mute_proc(self, context: dict, collapse=False, log=True, respond=True):
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                target_name=ctx.get("target_nametag"),
                now_time=ctx.get("now_time"),
                target_time=ctx.get("target_time")
            )
            self.logger.compose_log_attachments(
                peer_id=ctx.get("peer_id"),
                cmids=ctx.get("cmids")
            )

            # отправляем лог
            await self.logger.log()

        async def send_respond(ctx):
            rsn = f"Причина: {ctx.get('reason')} \n"
            text = f"@id{ctx.get('target_id')} (Пользователь) временно заглушен.\n" \
                   f"Повторная попытка отправить сообщение в чат приведёт к блокировке.\n" \
                   f"{rsn if ctx.get('reason') is not None else ''}" \
                   f"Время снятия заглушения: {self.converter.convert(ctx.get('target_time'))}\n" \
                   f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        is_muted = self.database.muted.select(
            ("target_name",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if not is_muted:
            role = self.database.permissions.select(
                ("target_lvl",),
                peer_id=context.get("peer_id"),
                target_id=context.get("initiator_id")
            )
            if role:
                role = role[0][0]
            else:
                role = 0
            context["initiator_lvl"] = role

            if respond:
                await send_respond(context)
            if log:
                await send_log(context)

            # выдаем мут
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
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                target_name=ctx.get("target_nametag"),
                now_time=ctx.get("now_time"),
                target_time=ctx.get("target_time")
            )
            self.logger.compose_log_attachments(
                peer_id=ctx.get("peer_id"),
                cmids=ctx.get("cmids")
            )

            # отправляем лог
            await self.logger.log()

        async def send_respond(ctx):
            text = f"@id{ctx.get('target_id')} (Пользователь) разглушен.\n"
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        is_muted = self.database.muted.select(
            ("target_name",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if is_muted:
            role = self.database.permissions.select(
                ("target_lvl",),
                peer_id=context.get("peer_id"),
                target_id=context.get("initiator_id")
            )
            if role:
                role = role[0][0]
            else:
                role = 0
            context["initiator_lvl"] = role

            if respond:
                await send_respond(context)
            if log:
                await send_log(context)

            self.database.muted.delete(
                peer_id=context.get("peer_id"),
                target_id=context.get("target_id")
            )

    async def warn_proc(self, context: dict, collapse=False, log=True, respond=True):
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                target_name=ctx.get("target_nametag"),
                target_warns=ctx.get("target_warns"),
                now_time=ctx.get("now_time"),
                target_time=ctx.get("target_time")
            )
            self.logger.compose_log_attachments(
                peer_id=ctx.get("peer_id"),
                cmids=ctx.get("cmids")
            )

            # отправляем лог
            await self.logger.log()

        async def send_respond(ctx):
            rsn = f"Причина: {ctx.get('reason')} \n"
            text = f"@id{ctx.get('target_id')} (Пользователь) получил предупреждение.\n" \
                   f"{rsn if ctx.get('reason') is not None else ''}" \
                   f"Текущее количество предупреждений: {ctx.get('target_warns')}/3.\n" \
                   f"Время снятия предупреждений: {self.converter.convert(ctx.get('target_time'))}\n" \
                   f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

            # выводим дельту времени

        role = self.database.permissions.select(
            ("target_lvl",),
            peer_id=context.get("peer_id"),
            target_id=context.get("initiator_id")
        )
        if role:
            role = role[0][0]
        else:
            role = 0
        context["initiator_lvl"] = role

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
            await send_respond(context)
        if log:
            await send_log(context)

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
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                target_name=ctx.get("target_nametag"),
                target_warns=ctx.get("target_warns"),
                now_time=ctx.get("now_time")
            )
            self.logger.compose_log_attachments(
                peer_id=ctx.get("peer_id"),
                cmids=ctx.get("cmids")
            )

            # отправляем лог
            await self.logger.log()

        async def send_respond(ctx):
            text = f"С @id{ctx.get('target_id')} (пользователя) снято предупреждение.\n"
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        role = self.database.permissions.select(
            ("target_lvl",),
            peer_id=context.get("peer_id"),
            target_id=context.get("initiator_id")
        )
        if role:
            role = role[0][0]
        else:
            role = 0
        context["initiator_lvl"] = role

        warns = self.database.warned.select(
            ("warn_count",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if warns:
            warns = warns[0][0]
        else:
            warns = 0
        context["target_warns"] = warns - 1

        if respond:
            await send_respond(context)
        if log:
            await send_log(context)

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
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_role"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                now_time=ctx.get("now_time"),
            )
            self.logger.compose_log_attachments(
                peer_id=ctx.get("peer_id"),
                cmids=ctx.get("cmids")
            )

            # отправляем лог
            await self.logger.log()

        async def send_respond(ctx):
            text = ctx.get("copied")
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        role = self.database.permissions.select(
            ("target_lvl",),
            peer_id=context.get("peer_id"),
            target_id=context.get("initiator_id")
        )
        if role:
            role = role[0][0]
        else:
            role = 0
        context["initiator_lvl"] = role

        if respond:
            await send_respond(context)
        if log:
            await send_log(context)

    async def delete_proc(self, context: dict, log=True, respond=True):
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_role"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                now_time=ctx.get("now_time"),
            )
            self.logger.compose_log_attachments(
                peer_id=ctx.get("peer_id"),
                cmids=ctx.get("cmids")
            )

            # отправляем лог
            await self.logger.log()

        async def send_respond(ctx):
            text = "Сообщение(я) удалены."
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        role = self.database.permissions.select(
            ("target_lvl",),
            peer_id=context.get("peer_id"),
            target_id=context.get("initiator_id")
        )
        if role:
            role = role[0][0]
        else:
            role = 0
        context["initiator_lvl"] = role

        if respond:
            await send_respond(context)
        if log:
            await send_log(context)

        try:
            await self.bot.api.messages.delete(
                group_id=GROUP_ID,
                peer_id=context.get("peer_id"),
                cmids=context.get("cmids"),
                delete_for_all=True
            )

        except Exception as error:
            print("Process aborted:", error)
            return

    async def setting_proc(self, context: dict, log=True, respond=True):
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_role"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                setting_name=ctx.get("setting_name"),
                setting_status=ctx.get("setting_status"),
                now_time=ctx.get("now_time"),
            )

            # отправляем лог
            await self.logger.log()

        async def send_respond(ctx):
            text = f"Настройка {ctx.get('setting_name')} для этой беседы изменена на {ctx.get('setting_status')}\n"
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        is_setting = self.database.settings.select(
            ("setting_name",),
            peer_id=context.get("peer_id"),
            setting_name=context.get("setting_name")
        )
        if is_setting:
            role = self.database.permissions.select(
                ("target_lvl",),
                peer_id=context.get("peer_id"),
                target_id=context.get("initiator_id")
            )
            if role:
                role = role[0][0]
            else:
                role = 0
            context["initiator_lvl"] = role

            self.database.settings.update(
                {"setting_status": context.get("setting_status")},
                peer_id=context.get("peer_id"),
                setting_name=context.get("setting_name")
            )

            if respond:
                await send_respond(context)
            if log:
                await send_log(context)

    async def queue_proc(self, context: dict, log=True, respond=True):
        async def send_log(ctx):
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_role"),
                peer_name=ctx.get("peer_name"),
                target_name=ctx.get("target_nametag"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                now_time=ctx.get("now_time"),
            )
            self.logger.compose_log_attachments(
                peer_id=ctx.get("peer_id"),
                cmids=ctx.get("cmids")
            )
            await self.logger.log()

        async def send_respond(ctx):
            text = f"@id{ctx.get('target_id')} (Пользователь) добавлен в очередь.\n"
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        role = self.database.permissions.select(
            ("target_lvl",),
            peer_id=context.get("peer_id"),
            target_id=context.get("initiator_id")
        )
        if role:
            role = role[0][0]
        else:
            role = 0
        context["initiator_lvl"] = role

        if respond:
            await send_respond(context)
        if log:
            await send_log(context)

        self.database.queue.insert(
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id"),
            target_name=context.get("target_name"),
            send_time=context.get("now_time"),
            next_time=context.get("target_time")
        )

    async def unqueue_proc(self, context: dict, log=True, respond=True):
        async def send_log(ctx):
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_role"),
                peer_name=ctx.get("peer_name"),
                target_name=ctx.get("target_nametag"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                now_time=ctx.get("now_time"),
            )

            await self.logger.log()

        async def send_respond(ctx):
            text = f"@id{ctx.get('target_id')} (Пользователь) удален из очереди.\n"
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        role = self.database.permissions.select(
            ("target_lvl",),
            peer_id=context.get("peer_id"),
            target_id=context.get("initiator_id")
        )
        if role:
            role = role[0][0]
        else:
            role = 0
        context["initiator_lvl"] = role

        if respond:
            await send_respond(context)
        if log:
            await send_log(context)

        self.database.queue.delete(
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id"),
        )


class InformationProcessor(StdProcessor, metaclass=MetaSingleton):
    async def _send_respond(self, text, ctx):
        await self.bot.api.messages.send(
            chat_id=ctx.get("chat_id"),
            message=text,
            random_id=0
        )

    async def info_permission_proc(self, context):
        conversations = self.database.conversations.select(
            ("peer_id",),
            peer_type="CHAT"
        )
        conversations = [peer_id[0] for peer_id in conversations]

        for peer_id in conversations:
            peer_name = await self.info.peer_name(peer_id)
            text = f"{peer_name} | Роли: \n"

            users = self.database.permissions.select(
                ("target_name", "target_lvl"),
                peer_id=peer_id
            )
            for name, role in users:
                text += f"* {name} -- {role}:{PERMISSION_LVL[role]}\n"

            await self._send_respond(text, context)

    async def info_setting_proc(self, context):
        conversations = self.database.conversations.select(
            ("peer_id",),
            peer_type="CHAT"
        )
        conversations = [peer_id[0] for peer_id in conversations]

        for peer_id in conversations:
            peer_name = await self.info.peer_name(peer_id)
            text = f"{peer_name} | Настройки: \n"

            settings = self.database.settings.select(
                ("setting_name", "setting_status"),
                peer_id=peer_id
            )
            for name, status in settings:
                text += f"* {name} -- {status}\n"

            await self._send_respond(text, context)

    async def info_chat_proc(self, context):
        conversations = self.database.conversations.select(
            ("peer_name", "peer_type")
        )
        text = "Зарегистрированные беседы: \n"
        for cname, ctype in conversations:
            text += f"* {cname} -- {ctype} \n"

        await self._send_respond(text, context)

    async def info_kick_proc(self, context):
        conversations = self.database.conversations.select(
            ("peer_id",),
            peer_type="CHAT"
        )
        conversations = [peer_id[0] for peer_id in conversations]

        for peer_id in conversations:
            peer_name = await self.info.peer_name(peer_id)
            text = f"{peer_name} | Исключенные пользователи: \n"

            kicks = self.database.kicked.select(
                ("initiator_name", "target_name", "kick_time"),
                peer_id=peer_id
            )
            for initiator_name, target_name, kick_time in kicks:
                text += f"* {target_name} -- {self.converter.convert(kick_time)}\n" \
                        f"\\-Инициатор: {target_name}\n"

            await self._send_respond(text, context)

    async def info_ban_proc(self, context):
        conversations = self.database.conversations.select(
            ("peer_id",),
            peer_type="CHAT"
        )
        conversations = [peer_id[0] for peer_id in conversations]

        for peer_id in conversations:
            peer_name = await self.info.peer_name(peer_id)
            text = f"{peer_name} | Заблокированные пользователи: \n"

            bans = self.database.banned.select(
                ("initiator_name", "target_name", "ban_time", "unban_time"),
                peer_id=peer_id
            )
            for initiator_name, target_name, ban_time, unban_time in bans:
                text += f"* {target_name} -- {self.converter.convert(ban_time)}\n" \
                        f"|-Время снятия: {self.converter.convert(unban_time)}\b" \
                        f"\\-Инициатор: {target_name}\n"

            await self._send_respond(text, context)

    async def info_mute_proc(self, context):
        conversations = self.database.conversations.select(
            ("peer_id",),
            peer_type="CHAT"
        )
        conversations = [peer_id[0] for peer_id in conversations]

        for peer_id in conversations:
            peer_name = await self.info.peer_name(peer_id)
            text = f"{peer_name} | Заглушенные пользователи: \n"

            mutes = self.database.muted.select(
                ("initiator_name", "target_name", "mute_time", "unmute_time"),
                peer_id=peer_id
            )
            for initiator_name, target_name, mute_time, unmute_time in mutes:
                text += f"* {target_name} -- {self.converter.convert(mute_time)}\n" \
                        f"|-Время снятия: {self.converter.convert(unmute_time)}\b" \
                        f"\\-Инициатор: {target_name}\n"

            await self._send_respond(text, context)

    async def info_warn_proc(self, context):
        conversations = self.database.conversations.select(
            ("peer_id",),
            peer_type="CHAT"
        )
        conversations = [peer_id[0] for peer_id in conversations]

        for peer_id in conversations:
            peer_name = await self.info.peer_name(peer_id)
            text = f"{peer_name} | Заглушенные пользователи: \n"

            warns = self.database.muted.select(
                ("initiator_name", "target_name", "warn_time", "unwarn_time", "warn_count"),
                peer_id=peer_id
            )
            for initiator_name, target_name, warn_time, unwarn_time, warn_count in warns:
                text += f"* {target_name} -- {self.converter.convert(warn_time)}\n" \
                        f"|- Время снятия: {self.converter.convert(unwarn_time)}\b" \
                        f"|- Количество предупреждений: {warn_count}\n" \
                        f"\\- Инициатор: {target_name}\n"

            await self._send_respond(text, context)


class ReferenceProcessor(StdProcessor, metaclass=MetaSingleton):
    async def _send_respond(self, text, ctx):
        await self.bot.api.messages.send(
            chat_id=ctx.get("chat_id"),
            message=text,
            random_id=0
        )

    async def ref_all_proc(self, context):
        url_tech = "https://github.com/STALCRAFT-FUNCKA/TOASTER/blob/release/README.md"
        url_upd = "https://github.com/STALCRAFT-FUNCKA/TOASTER/releases"
        text = f"Документация: \n {url_tech} \n" \
               f"Обновления: \n {url_upd} \n"

        await self._send_respond(text, context)

    async def ref_reference_proc(self, context):
        text = "/reference \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['reference']} \n"\
              f"* Доступ для группы прав {PERMISSION_ACCESS['reference']} уровня или выше \n" \
               "* Может быть вызвана только в лог-чате\n" \
               "\n" \
               "Опиcание: Выводит в чат справочную информацию по какой-либо команде."

        await self._send_respond(text, context)

    async def ref_chat_proc(self, context):
        text = "/chat \n" \
               "* Доступные префиксы: ! или / \n" \
               f"* Псевдонимы команды: {ALIASES['chat']} \n" \
               f"* Доступ для группы прав {PERMISSION_ACCESS['chat']} уровня или выше \n" \
               "\n" \
               "Описание: Команда помечает беседу, как чат. " \
               "Теперь в этой беседе будет проходить модерация фильтрами."

        await self._send_respond(text, context)

    async def ref_log_proc(self, context):
        text = "/log \n" \
               "* Доступные префиксы: ! или / \n" \
               f"* Псевдонимы команды: {ALIASES['log']} \n" \
               f"* Доступ для группы прав {PERMISSION_ACCESS['log']} уровня или выше \n" \
               "\n" \
               "Описание: Команда помечает беседу, как лог-чат. " \
               "Теперь в эту беседу будут приходить логи исполненных команд."

        await self._send_respond(text, context)

    async def ref_drop_proc(self, context):
        text = "/drop \n" \
               "* Доступные префиксы: ! или / \n" \
               f"* Псевдонимы команды: {ALIASES['drop']} \n" \
               f"* Доступ для группы прав {PERMISSION_ACCESS['drop']} уровня или выше \n" \
               "\n" \
               "Описание: Команда сбрасывает метку чата или лог-чата с беседы."

        await self._send_respond(text, context)

    async def ref_permission_proc(self, context):
        text = "/permission <lvl> <@user|optional> \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['permission']} \n" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['permission']} уровня или выше \n" \
               "* Может быть вызвана в лог-чате \n" \
               "\n" \
               "Описание: Команда устанавливает для пользователя группу прав, равную введенному аргументу.\n" \
               "\n" \
               "Доступные аргументы: \n" \
               "* <lvl>: 0 (user), 1 (moderator), 2 (administrator)"

        await self._send_respond(text, context)

    async def ref_setting_proc(self, context):
        text = "/permission <setting> <value> \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['setting']} \n" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['setting']} уровня или выше \n" \
               "\n" \
               "Описание: Переключает настройку беседы. Каждая настройка приводит или выводит из действия фильтр, " \
               "отвечающий за тот или иной контент.\n" \
               "\n" \
               "Доступные аргументы: \n" \
               "* <value>: True\\False \n" \
               "* <setting>: Allow_Picture, Allow_Video, Allow_Music, Allow_Voice, Allow_Post, Allow_Votes, " \
               "Allow_Files, Allow_Miniapp, Allow_Graffiti, Allow_Sticker, Allow_Reply, Filter_Curse, Slow_Mode, " \
               "Account_Age, Hard_Mode"

        await self._send_respond(text, context)

    async def ref_delete_proc(self, context):
        text = "/delete \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['delete']} \n" \
              f"* Обработка только совместно с пересланным сообщением" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['delete']} уровня или выше \n" \
               "* Может быть вызвана в лог-чате \n" \
               "\n" \
               "Описание: Удаляет пересланное или группу пересланных сообщений.\n" \

        await self._send_respond(text, context)

    async def ref_copy_proc(self, context):
        text = "/copy \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['copy']} \n" \
              f"* Обработка только совместно с пересланным сообщением" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['copy']} уровня или выше \n" \
               "* Может быть вызвана в лог-чате \n" \
               "\n" \
               "Описание: Копирует текст пересланного сообщения и отправляет в беседу от лица бота.\n" \

        await self._send_respond(text, context)

    async def ref_terminate_proc(self, context):
        text = "/terminate <@user|optional> \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['terminate']} \n" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['terminate']} уровня или выше \n" \
               "\n" \
               "Описание: Исключает пользователя из всех бесед навсегда.\n" \

        await self._send_respond(text, context)

    async def ref_kick_proc(self, context):
        text = "/kick <@user|optional> \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['kick']} \n" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['kick']} уровня или выше \n" \
               "\n" \
               "Описание: Исключает пользователя из беседы навсегда.\n" \

        await self._send_respond(text, context)

    async def ref_ban_proc(self, context):
        text = "/ban <time> <coefficent> <@user|optional> \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['ban']} \n" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['ban']} уровня или выше \n" \
              f"* Может быть вызвана только в чате \n" \
               "\n" \
               "Описание: Блокирует пользователя на некоторый промежуток времени и удаляет из чата. " \
               "Уведомление об окончании блокировки поступит в лог-чаты.\n" \
               "\n" \
               "Доступные аргументы: \n" \
               "* <time>: натуральное число \n" \
               "* <coefficent>: h (hour), d (day), m (month)"

        await self._send_respond(text, context)

    async def ref_unban_proc(self, context):
        text = "/unban <@user|optional> \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['unban']} \n" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['unban']} уровня или выше \n" \
              f"* Может быть вызвана только в чате \n" \
               "\n" \
               "Описание: Снимает с пользователя блокировку.\n"

        await self._send_respond(text, context)

    async def ref_mute_proc(self, context):
        text = "/mute <time> <coefficent> <@user|optional> \n" \
               "* Доступные префиксы: ! или / \n" \
               f"* Псевдонимы команды: {ALIASES['mute']} \n" \
               f"* Доступ для группы прав {PERMISSION_ACCESS['mute']} уровня или выше \n" \
               f"* Может быть вызвана только в чате \n" \
               "\n" \
               "Описание: Заглушает пользователя на некоторый промежуток времени. " \
               "При нарушении заглушения пользователь блокируется на день. " \
               "Уведомление об окончании заглушения поступит в лог-чаты.\n" \
               "\n" \
               "Доступные аргументы: \n" \
               "* <time>: натуральное число \n" \
               "* <coefficent>: h (hour), d (day), m (month)"

        await self._send_respond(text, context)

    async def ref_unmute_proc(self, context):
        text = "/unmute <@user|optional> \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['unmute']} \n" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['unmute']} уровня или выше \n" \
              f"* Может быть вызвана только в чате \n" \
               "\n" \
               "Описание: Снимает с пользователя заглушение.\n"

        await self._send_respond(text, context)

    async def ref_warn_proc(self, context):
        text = "/warn <@user|optional> \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['warn']} \n" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['warn']} уровня или выше \n" \
              f"* Может быть вызвана только в чате \n" \
               "\n" \
               "Описание: Выдает пользователю одно предупреждение. " \
               "По достижении 3-х предупреждений пользователь получит мут на день. " \
               "Все предупреждения снимаются по истечению 24 часов с момента получения последнего предупреждения. " \
               "Уведомление о снятии предупреждений поступит в лог-чаты.\n"

        await self._send_respond(text, context)

    async def ref_unwarn_proc(self, context):
        text = "/unwarn <@user|optional> \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['unwarn']} \n" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['unwarn']} уровня или выше \n" \
              f"* Может быть вызвана только в чате \n" \
               "\n" \
               "Описание: Снимает с пользователя одно предупреждение.\n"

        await self._send_respond(text, context)

    async def ref_queue_proc(self, context):
        text = "/queue <@user|optional> \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['queue']} \n" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['queue']} уровня или выше \n" \
              f"* Может быть вызвана только в чате \n" \
               "\n" \
               "Описание: Добавляет пользователя в очередь сообщений медленного режима.\n"

        await self._send_respond(text, context)

    async def ref_unqueue_proc(self, context):
        text = "/unqueue <@user|optional> \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['unqueue']} \n" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['unqueue']} уровня или выше \n" \
              f"* Может быть вызвана только в чате \n" \
               "\n" \
               "Описание: Удаляет пользователя из очереди сообщений медленного режима.\n"

        await self._send_respond(text, context)

    async def ref_info_proc(self, context):
        text = "/info <list_name> \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['info']} \n" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['info']} уровня или выше \n" \
              f"* Может быть вызвана только в лог-чате \n" \
               "\n" \
               "Описание: Выводит информацию о текущем состоянии указанного списка объектов.\n" \
               "\n" \
               "Доступные аргументы: \n" \
               "* <list_name>: permission, setting, chat, kick, ban, mute, warn"

        await self._send_respond(text, context)
