"""
В этом файле описаны основные функции, которые отвечают за взаимодействие с базой данных и выдачу наказаний.
Функции-процессоры включают в себя не только взаимодействие с БД, но и отправку логов (респондов).
Основным способом обмена информацией для функций-процессоров является словарь:Dict:.
"""
from vkbottle import Bot
from config import TOKEN, STUFF_ADMIN_ID, PERMISSION_LVL
from database.orm import DataBase
from utils import *


# TODO: Пофиксить роли в логах
class Processor:
    def __init__(self):
        self.logger = Logger()

        self.bot = Bot(token=TOKEN)
        self.database = DataBase()
        # Подключениек ORM\DB

    async def enroll_proc(self):
        ...

    async def enroll_log_proc(self):
        ...

    async def drop_proc(self):
        ...

    async def drop_log_proc(self):
        ...

    async def terminate_proc(self):
        ...

    async def kick_proc(self, context: dict, log=True, respond=True):
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                target_name=ctx.get("target_nametag"),
                command_name=ctx.get("command_name"),
                now_time=ctx.get("now_time")
            )
            self.logger.compose_log_attachments(
                peer_id=ctx.get("peer_id"),
                cmids=ctx.get("cmids")
            )

            # отправляем лог
            await self.logger.log()

        async def send_respond(ctx):
            text = f"@id{ctx.get('target_id')} (Пользователь) исключен из беседы.\n" \
                    f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        # проверяем наличие пользователя в бд
        is_kicked = all(
            self.database.kicked.select(
                ("target_name",),
                peer_id=context.get("peer_id"),
                user_id=context.get("target_id")
            )
        )
        if not is_kicked:
            role = self.database.permissions.select(
                ("initiator_lvl",),
                peer_id=context.get("peer_id"),
                user_id=context.get("target_id")
            )
            if role:
                role = role[0][0]
            else:
                role = 0
            context["initiator_lvl"] = f"{role} - {PERMISSION_LVL[role]}"

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

            await self.bot.api.messages.remove_chat_user(
                chat_id=context.get("chat_id"),
                user_id=context.get("target_id")
            )

    async def ban_proc(self, context: dict, log=True, respond=True):
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
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
            text = f"@id{ctx.get('target_id')} (Пользователь) временно заблокирован.\n" \
                    f"Время снятия блокировки: {ctx.get('target_time')}\n" \
                    f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        is_banned = all(
            self.database.banned.select(
                ("target_name",),
                peer_id=context.get("peer_id"),
                user_id=context.get("target_id")
            )
        )
        if not is_banned:
            role = self.database.permissions.select(
                ("initiator_lvl",),
                peer_id=context.get("peer_id"),
                user_id=context.get("target_id")
            )
            if role:
                role = role[0][0]
            else:
                role = 0
            context["initiator_lvl"] = f"{role} - {PERMISSION_LVL[role]}"

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

            await self.bot.api.messages.remove_chat_user(
                chat_id=context.get("chat_id"),
                user_id=context.get("target_id")
            )

    async def unban_proc(self, context: dict, log=True, respond=True):
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                target_name=ctx.get("target_nametag"),
                now_time=ctx.get("now_time"),
            )

            # отправляем лог
            await self.logger.log()

            # получаем все необходимые данные

        async def send_respond(ctx):
            text = f"@id{ctx.get('target_id')} (Пользователь) разблокирован.\n"
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        is_banned = all(
            self.database.banned.select(
                ("target_name",),
                peer_id=context.get("peer_id"),
                target_id=context.get("target_id")
            )
        )
        if is_banned:
            role = self.database.permissions.select(
                ("initiator_lvl",),
                peer_id=context.get("peer_id"),
                user_id=context.get("target_id")
            )
            if role:
                role = role[0][0]
            else:
                role = 0
            context["initiator_lvl"] = f"{role} - {PERMISSION_LVL[role]}"

            if respond:
                await send_respond(context)
            if log:
                await send_log(context)

            self.database.banned.delete(
                peer_id=context.get("peer_id"),
                target_id=context.get("target_id")
            )

    async def mute_proc(self, context: dict, log=True, respond=True):
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
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
            text = f"@id{ctx.get('target_id')} (Пользователь) временно заглушен.\n" \
                    f"Повторная попытка отправить сообщение в чат приведёт к блокировке.\n" \
                    f"Время снятия заглушения: {ctx.get('target_time')}\n" \
                    f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

        is_muted = all(
            self.database.muted.select(
                ("target_name",),
                peer_id=context.get("peer_id"),
                user_id=context.get("target_id")
            )
        )
        if not is_muted:
            role = self.database.permissions.select(
                ("initiator_lvl",),
                peer_id=context.get("peer_id"),
                user_id=context.get("target_id")
            )
            if role:
                role = role[0][0]
            else:
                role = 0
            context["initiator_lvl"] = f"{role} - {PERMISSION_LVL[role]}"

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

    async def unmute_proc(self, context: dict, log=True, respond=True):
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
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

        is_muted = all(
            self.database.muted.select(
                ("target_name",),
                peer_id=context.get("peer_id"),
                user_id=context.get("target_id")
            )
        )
        if is_muted:
            role = self.database.permissions.select(
                ("initiator_lvl",),
                peer_id=context.get("peer_id"),
                user_id=context.get("target_id")
            )
            if role:
                role = role[0][0]
            else:
                role = 0
            context["initiator_lvl"] = f"{role} - {PERMISSION_LVL[role]}"

            if respond:
                await send_respond(context)
            if log:
                await send_log(context)

            self.database.muted.delete(
                peer_id=context.get("peer_id"),
                target_id=context.get("target_id")
            )
            
    async def warn_proc(self, context: dict, log=True, respond=True):
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
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
            text = f"@id{ctx.get('target_id')} (Пользователь) получил предупреждение.\n" \
                    f"Текущее количество предупреждений: {ctx.get('target_warns')}/3.\n" \
                    f"Время снятия предупреждений: {ctx.get('target_time')}\n" \
                    f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
            await self.bot.api.messages.send(
                chat_id=ctx.get("chat_id"),
                message=text,
                random_id=0
            )

            # выводим дельту времени

        role = self.database.permissions.select(
            ("initiator_lvl",),
            peer_id=context.get("peer_id"),
            user_id=context.get("target_id")
        )
        if role:
            role = role[0][0]
        else:
            role = 0
        context["initiator_lvl"] = f"{role} - {PERMISSION_LVL[role]}"

        warns = self.database.warned.select(
            ("warn_count",),
            peer_id=context.get("peer_id"),
            user_id=context.get("target_id")
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

    async def unwarn_proc(self, context: dict, force=False, log=True, respond=True):
        async def send_log(ctx):
            # формируем лог
            self.logger.compose_log_data(
                initiator_name=ctx.get("initiator_nametag"),
                initiator_role=ctx.get("initiator_lvl"),
                peer_name=ctx.get("peer_name"),
                command_name=ctx.get("command_name"),
                target_name=ctx.get("target_name_ag"),
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
            ("initiator_lvl",),
            peer_id=context.get("peer_id"),
            user_id=context.get("target_id")
        )
        if role:
            role = role[0][0]
        else:
            role = 0
        context["initiator_lvl"] = f"{role} - {PERMISSION_LVL[role]}"

        warns = self.database.warned.select(
            ("warn_count",),
            peer_id=context.get("peer_id"),
            user_id=context.get("target_id")
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

    async def copy_proc(self):
        ...

    async def delete_proc(self):
        ...

    async def setting_proc(self):
        ...