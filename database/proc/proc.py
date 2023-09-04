from vkbottle import Bot
from config import TOKEN, STUFF_ADMIN_ID, PERMISSION_LVL, GROUP_ID, SETTINGS, QUEUE_TIME
from database.orm import DataBase
from database.proc.logger import Logger
from singltone import MetaSingleton
from utils import Converter


class Processor(metaclass=MetaSingleton):
    __debug = False

    # Если этот параметр True - то пользователя не исключит из беседы, при исполнении процессов бана, кика и т.п.

    def __init__(self):
        self.logger = Logger()
        self.converter = Converter()

        self.bot = Bot(token=TOKEN)
        self.database = DataBase()

    async def reference_proc(self, context, log=True, respond=True):
        async def send_log(ctx):
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                reason=ctx.get("reason", None),
                now_time=ctx.get("now_time")
            )

            await self.logger.log()

        async def send_respond(ctx):
            url_tech = "https://github.com/STALCRAFT-FUNCKA/TOASTER/blob/release/README.md"
            url_upd = "https://github.com/STALCRAFT-FUNCKA/TOASTER/releases/tag/v2.0.4"
            text = f"Документация: \n {url_tech} \n" \
                   f"Обновления: \n {url_upd} \n"
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        role = self.database.permissions.select(
            ("target_lvl",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
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
            target_id=context.get("target_id")
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
            target_id=context.get("target_id")
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
                target_id=context.get("target_id")
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
            if log:
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
            target_id=context.get("target_id")
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
            target_id=context.get("target_id")
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
                target_id=context.get("target_id")
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
                target_id=context.get("target_id")
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
                target_id=context.get("target_id")
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
                target_id=context.get("target_id")
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
                target_id=context.get("target_id")
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
            target_id=context.get("target_id")
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
            target_id=context.get("target_id")
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
            target_id=context.get("target_id")
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
            target_id=context.get("target_id")
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
                target_id=context.get("target_id")
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
            target_id=context.get("target_id")
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
            next_time=context.get("now_time") + QUEUE_TIME
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
            target_id=context.get("target_id")
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
