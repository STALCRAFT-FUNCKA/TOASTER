from vkbottle import Bot
from config import (
    PERMISSION_LVL,
    SETTINGS,
    PERMISSION_ACCESS,
    TOKEN,
    STAFF_ADMIN_ID,
    GROUP_ID,
    ALIASES
)
from data import DataBase
from .logger import Logger
from singltone import MetaSingleton
from utils import Converter, Informer


class StdProcessor:
    def __init__(self):
        self.bot = Bot(token=TOKEN)
        self.database = DataBase()
        self.logger = Logger()
        self.info = Informer()
        self.converter = Converter()

    async def _send_respond(self, text, ctx, highlighter=False):
        if highlighter:
            text = "---------------------------------------------- \n" + text
            text = text + "----------------------------------------------"
        await self.bot.api.messages.send(
            chat_id=ctx.get("chat_id"),
            message=text,
            random_id=0
        )

    async def _send_log(self, ctx, highlighter=False):
        self.logger.compose_log_data(ctx)
        self.logger.compose_log_attachments(ctx)
        await self.logger.log(highlighter=highlighter)

    def _get_initiator_lvl(self, context):
        role = self.database.permissions.select(
            ("target_lvl",),
            peer_id=context.get("peer_id"),
            target_id=context.get("initiator_id")
        )
        if role:
            return role[0][0]
        else:
            return 0


class CommandProcessor(StdProcessor, metaclass=MetaSingleton):
    __debug = False

    async def chat_proc(self, context, log=True, respond=True):
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

        if k:
            for name, status in SETTINGS.items():
                print(name, status)
                self.database.settings.insert(
                    peer_id=context.get("peer_id"),
                    setting_name=name,
                    setting_status=status
                )

            self.database.permissions.insert(
                peer_id=context.get("peer_id"),
                target_id=0,
                target_name="Система",
                target_lvl=2
            )

    async def log_proc(self, context: dict, log=True, respond=True):
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

    async def terminate_proc(self, context: dict, collapse=False, log=True, respond=True):
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
                    text = f"@id{context.get('target_id')} (Пользователь) исключен из всех бесед навсегда.\n" \
                            f"По вопросам обращаться к @id{STAFF_ADMIN_ID} (Администратору).\n"
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
        context["initiator_lvl"] = self._get_initiator_lvl(context)

        if respond:
            text = f"@id{context.get('target_id')} (Пользователю) установлена роль {context.get('target_lvl')}" \
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
        is_kicked = self.database.kicked.select(
            ("target_name",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if not is_kicked:
            context["initiator_lvl"] = self._get_initiator_lvl(context)

            if respond:
                rsn = f"Причина: {context.get('reason')} \n"
                text = f"@id{context.get('target_id')} (Пользователь) исключен из беседы.\n" \
                       f"{rsn if context.get('reason') is not None else ''}" \
                       f"По вопросам обращаться к @id{STAFF_ADMIN_ID} (Администратору).\n"
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
        is_banned = self.database.banned.select(
            ("target_name",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if not is_banned:
            context["initiator_lvl"] = self._get_initiator_lvl(context)

            if respond:
                rsn = f"Причина: {context.get('reason')} \n"
                text = f"@id{context.get('target_id')} (Пользователь) временно заблокирован.\n" \
                       f"{rsn if context.get('reason') is not None else ''}" \
                       f"Время снятия блокировки: {self.converter.convert(context.get('target_time'))}\n" \
                       f"По вопросам обращаться к @id{STAFF_ADMIN_ID} (Администратору).\n"
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
        is_muted = self.database.muted.select(
            ("target_name",),
            peer_id=context.get("peer_id"),
            target_id=context.get("target_id")
        )
        if not is_muted:
            context["initiator_lvl"] = self._get_initiator_lvl(context)

            if respond:
                rsn = f"Причина: {context.get('reason')} \n"
                text = f"@id{context.get('target_id')} (Пользователь) временно заглушен.\n" \
                       f"Повторная попытка отправить сообщение в чат приведёт к блокировке.\n" \
                       f"{rsn if context.get('reason') is not None else ''}" \
                       f"Время снятия заглушения: {self.converter.convert(context.get('target_time'))}\n" \
                       f"По вопросам обращаться к @id{STAFF_ADMIN_ID} (Администратору).\n"
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
            text = f"@id{context.get('target_id')} (Пользователь) получил предупреждение.\n" \
                   f"{rsn if context.get('reason') is not None else ''}" \
                   f"Текущее количество предупреждений: {context.get('target_warns')}/3.\n" \
                   f"Время снятия предупреждений: {self.converter.convert(context.get('target_time'))}\n" \
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
            text = f"С @id{context.get('target_id')} (пользователя) снято предупреждение.\n"
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
        context["initiator_lvl"] = self._get_initiator_lvl(context)

        if respond:
            text = "Сообщение скопировано"
            await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        text = context.get("copied") + "\n"
        await self._send_respond(text, context)

    async def delete_proc(self, context: dict, log=True, respond=True):
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

        except Exception as error:
            print("Process aborted:", error)
            return

    async def setting_proc(self, context: dict, log=True, respond=True):
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
                text = f"Настройка {context.get('setting_name')} для этой беседы изменена на " \
                       f"{context.get('setting_status')}\n"
                await self._send_respond(text, context)
            if log:
                await self._send_log(context)

    async def queue_proc(self, context: dict, log=True, respond=True):
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


class InformationProcessor(StdProcessor, metaclass=MetaSingleton):
    async def info_permission_proc(self, context):
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
                ("initiator_name", "target_name", "warn_time", "unwarn_time", "warn_count"),
                peer_id=peer_id
            )
            for initiator_name, target_name, warn_time, unwarn_time, warn_count in warns:
                text += f"* {target_name} -- {self.converter.convert(warn_time)}\n" \
                        f"|- Время снятия: {self.converter.convert(unwarn_time)}\n" \
                        f"|- Количество предупреждений: {warn_count}\n" \
                        f"\\- Инициатор: {initiator_name}\n"

            if text != title:
                await self._send_respond(text, context)


class ReferenceProcessor(StdProcessor, metaclass=MetaSingleton):
    async def ref_all_proc(self, context):
        url_tech = "https://github.com/STALCRAFT-FUNCKA/TOASTER/blob/release/README.md"
        url_upd = "https://github.com/STALCRAFT-FUNCKA/TOASTER/releases"
        text = f"Документация: \n {url_tech} \n" \
               f"Обновления: \n {url_upd} \n"

        await self._send_respond(text, context)

    async def ref_reference_proc(self, context):
        text = "/reference <command_name>\n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['reference']} \n"\
              f"* Доступ для группы прав {PERMISSION_ACCESS['reference']} уровня или выше \n" \
               "* Может быть вызвана только в лог-чате\n" \
               "\n" \
               "Опиcание: Выводит в чат справочную информацию по какой-либо команде. \n" \
               "\n" \
               "Доступные аргументы: \n" \
               "* <command_name>: all (вывод общей справки) или любая команда, включая ее псевдонимы \n"

        await self._send_respond(text, context)

    async def ref_mark_proc(self, context):
        text = "/mark <arg> \n" \
               "* Доступные префиксы: ! или / \n" \
               f"* Псевдонимы команды: {ALIASES['mark']} \n" \
               f"* Доступ для группы прав {PERMISSION_ACCESS['mark']} уровня или выше \n" \
               "\n" \
               "Описание: Команда помечает беседу лог-чатом или чатом. Так же метку чата можно сбросить. \n" \
               "\n" \
               "Доступные аргументы: \n" \
               "* <arg>: log, chat, drop \n"

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
               "* <lvl>: 0 (user), 1 (moderator), 2 (administrator)\n"

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
               "Account_Age, Hard_Mode\n"

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
               "* <coefficent>: h (hour), d (day), m (month)\n"

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
               "* <coefficent>: h (hour), d (day), m (month)\n"

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
               "* <list_name>: permission, setting, mark, kick, ban, mute, warn\n"

        await self._send_respond(text, context)

    async def ref_roll_proc(self, context):
        text = "/roll <inf|optional> <sup|optional> \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['roll']} \n" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['roll']} уровня или выше \n" \
              f"* Может быть вызвана только в чате \n" \
               "\n" \
               "Описание: Прокручивает рулетку и выдает случайное число 0-100. " \
               "Есть возможность самостоятельно задать нижний\\верхний предел числа.\n" \
               "\n" \
               "Доступные аргументы: \n" \
               "* <inf|optional>`: Нижний предел числа.\n" \
               "* <inf|optional>`: Верхний предел числа.\n"

        await self._send_respond(text, context)

    async def ref_say_proc(self, context):
        text = "/say** <text> \n" \
               "* Доступные префиксы: ! или / \n" \
              f"* Псевдонимы команды: {ALIASES['say']} \n" \
              f"* Доступ для группы прав {PERMISSION_ACCESS['say']} уровня или выше \n" \
              f"* Может быть вызвана только в чате \n" \
               "\n" \
               "Описание: Отправляет сообщение от лица бота с указанным текстом.\n" \
               "\n" \
               "Доступные аргументы: \n" \
               "* <text>: Текст сообщения. Любой текст, с учетом пробелов и спец. символов\n"

        await self._send_respond(text, context)


class FunProcessor(StdProcessor, metaclass=MetaSingleton):
    async def fun_roll_proc(self, context, log=True, respond=True):
        context["initiator_lvl"] = self._get_initiator_lvl(context)

        if respond:
            text = f"Кости кинуты!\n"
            await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        result_text = (f"{context.get('initiator_nametag')} выбивает число "
                       f"({context.get('down_border')}-{context.get('up_border')}): {context.get('result')}")

        await self.bot.api.messages.send(
            chat_id=context.get("chat_id"),
            message=result_text,
            random_id=0
        )

    async def fun_say_proc(self, context, log=True, respond=True):
        context["initiator_lvl"] = self._get_initiator_lvl(context)

        if respond:
            text = f"Сообщение отправлено.\n"
            await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        await self.bot.api.messages.send(
            chat_id=context.get("chat_id"),
            message=context.get("say_text"),
            random_id=0
        )

    async def fun_hate_soloma_proc(self, context, log=True, respond=True):
        context["initiator_lvl"] = self._get_initiator_lvl(context)

        if respond:
            text = f"Солома зачмырён.\n"
            await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        text = f"СОЛОМА ТЫ ТАКОЙ ЛОХ!!!"

        await self.bot.api.messages.send(
            chat_id=context.get("chat_id"),
            message=text,
            random_id=0
        )