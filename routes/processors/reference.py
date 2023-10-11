"""
This file contains a description of the processor classes.
A processor is an object that has a certain semantic set of methods
that execute the basic logic of actions inside the bot. In other words,
the logic of filters, commands, handlers, etc.
"""

from singltone import MetaSingleton
from config import (
    PERMISSION_ACCESS,
    ALIASES
)
from .core import StdProcessor


class ReferenceProcessor(StdProcessor, metaclass=MetaSingleton):
    """
    Implements basic methods that perform specific actions on the command context.
    """

    async def ref_all_proc(self, context):
        """
        Implements the logic of the /reference command.
        """

        url_tech = "https://github.com/STALCRAFT-FUNCKA/TOASTER/blob/release/README.md"
        url_upd = "https://github.com/STALCRAFT-FUNCKA/TOASTER/releases"
        text = f"Документация: \n {url_tech} \n" \
               f"Обновления: \n {url_upd} \n"

        await self._send_respond(text, context)

    async def ref_reference_proc(self, context):
        """
        Implements the logic of the /reference reference command.
        """

        text = "/reference <command_name>\n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['reference']} \n"\
            f"* Доступ для группы прав {PERMISSION_ACCESS['reference']} "\
            f"уровня или выше \n" \
            "* Может быть вызвана только в лог-чате\n" \
            "\n" \
            "Опиcание: Выводит в чат справочную информацию по какой-либо команде. \n" \
            "\n" \
            "Доступные аргументы: \n" \
            "* <command_name>: all (вывод общей справки) или любая команда, "\
            f"включая ее псевдонимы \n"

        await self._send_respond(text, context)

    async def ref_mark_proc(self, context):
        """
        Implements the logic of the /reference mark command.
        """

        text = "/mark <arg> \n" \
               "* Доступные префиксы: ! или / \n" \
               f"* Псевдонимы команды: {ALIASES['mark']} \n" \
               f"* Доступ для группы прав {PERMISSION_ACCESS['mark']} "\
                f"уровня или выше \n" \
               "\n" \
               "Описание: Команда помечает беседу лог-чатом или чатом. "\
                f"Так же метку чата можно сбросить. \n" \
               "\n" \
               "Доступные аргументы: \n" \
               "* <arg>: log, chat, drop \n"

        await self._send_respond(text, context)

    async def ref_permission_proc(self, context):
        """
        Implements the logic of the /reference permission command.
        """

        text = "/permission <lvl> <@user|optional> \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['permission']} \n" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['permission']} "\
            f"уровня или выше \n" \
            "* Может быть вызвана в лог-чате \n" \
            "\n" \
            "Описание: Команда устанавливает для пользователя группу прав, "\
            f"равную введенному аргументу.\n" \
            "\n" \
            "Доступные аргументы: \n" \
            "* <lvl>: 0 (user), 1 (moderator), 2 (administrator)\n"

        await self._send_respond(text, context)

    async def ref_setting_proc(self, context):
        """
        Implements the logic of the /reference setting command.
        """

        text = "/permission <setting> <value> \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['setting']} \n" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['setting']} "\
            f"уровня или выше \n" \
            "\n" \
            "Описание: Переключает настройку беседы. Каждая настройка приводит "\
            f"или выводит из действия фильтр, " \
            "отвечающий за тот или иной контент.\n" \
            "\n" \
            "Доступные аргументы: \n" \
            "* <value>: True\\False \n" \
            "* <setting>: Allow_Picture, Allow_Video, Allow_Music, "\
            f"Allow_Voice, Allow_Post, Allow_Votes, " \
            "Allow_Files, Allow_Miniapp, Allow_Graffiti, Allow_Sticker, "\
            f"Allow_Reply, Filter_Curse, Slow_Mode, " \
            "Account_Age, Hard_Mode\n"

        await self._send_respond(text, context)

    async def ref_delete_proc(self, context):
        """
        Implements the logic of the /reference delete command.
        """

        text = "/delete \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['delete']} \n" \
            f"* Обработка только совместно с пересланным сообщением" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['delete']} "\
            f"уровня или выше \n" \
            "* Может быть вызвана в лог-чате \n" \
            "\n" \
            "Описание: Удаляет пересланное или группу пересланных сообщений.\n" \

        await self._send_respond(text, context)

    async def ref_copy_proc(self, context):
        """
        Implements the logic of the /reference copy command.
        """

        text = "/copy \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['copy']} \n" \
            f"* Обработка только совместно с пересланным сообщением" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['copy']} уровня или выше \n" \
            "* Может быть вызвана в лог-чате \n" \
            "\n" \
            "Описание: Копирует текст пересланного сообщения и "\
            f"отправляет в беседу от лица бота.\n" \

        await self._send_respond(text, context)

    async def ref_terminate_proc(self, context):
        """
        Implements the logic of the /reference terminate command.
        """

        text = "/terminate <@user|optional> \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['terminate']} \n" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['terminate']} "\
            f"уровня или выше \n" \
            "\n" \
            "Описание: Исключает пользователя из всех бесед навсегда.\n" \

        await self._send_respond(text, context)

    async def ref_kick_proc(self, context):
        """
        Implements the logic of the /reference kick command.
        """

        text = "/kick <@user|optional> \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['kick']} \n" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['kick']} уровня или выше \n" \
            "\n" \
            "Описание: Исключает пользователя из беседы навсегда.\n" \

        await self._send_respond(text, context)

    async def ref_ban_proc(self, context):
        """
        Implements the logic of the /reference ban command.
        """

        text = "/ban <time> <coefficent> <@user|optional> \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['ban']} \n" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['ban']} уровня или выше \n" \
            f"* Может быть вызвана только в чате \n" \
            "\n" \
            "Описание: Блокирует пользователя на некоторый "\
            f"промежуток времени и удаляет из чата. " \
            "Уведомление об окончании блокировки поступит в лог-чаты.\n" \
            "\n" \
            "Доступные аргументы: \n" \
            "* <time>: натуральное число \n" \
            "* <coefficent>: h (hour), d (day), m (month)\n"

        await self._send_respond(text, context)

    async def ref_unban_proc(self, context):
        """
        Implements the logic of the /reference unban command.
        """

        text = "/unban <@user|optional> \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['unban']} \n" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['unban']} "\
            f"уровня или выше \n" \
            f"* Может быть вызвана только в чате \n" \
            "\n" \
            "Описание: Снимает с пользователя блокировку.\n"

        await self._send_respond(text, context)

    async def ref_mute_proc(self, context):
        """
        Implements the logic of the /reference mute command.
        """

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
        """
        Implements the logic of the /reference unmute command.
        """

        text = "/unmute <@user|optional> \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['unmute']} \n" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['unmute']} "\
            f"уровня или выше \n" \
            f"* Может быть вызвана только в чате \n" \
            "\n" \
            "Описание: Снимает с пользователя заглушение.\n"

        await self._send_respond(text, context)

    async def ref_warn_proc(self, context):
        """
        Implements the logic of the /reference warn command.
        """

        text = "/warn <@user|optional> \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['warn']} \n" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['warn']} уровня или выше \n" \
            f"* Может быть вызвана только в чате \n" \
            "\n" \
            "Описание: Выдает пользователю одно предупреждение. " \
            "По достижении 3-х предупреждений пользователь получит мут на день. " \
            "Все предупреждения снимаются по истечению 24 часов с момента получения "\
            f"последнего предупреждения. " \
            "Уведомление о снятии предупреждений поступит в лог-чаты.\n"

        await self._send_respond(text, context)

    async def ref_unwarn_proc(self, context):
        """
        Implements the logic of the /reference unwarn command.
        """

        text = "/unwarn <@user|optional> \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['unwarn']} \n" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['unwarn']} "\
            f"уровня или выше \n" \
            f"* Может быть вызвана только в чате \n" \
            "\n" \
            "Описание: Снимает с пользователя одно предупреждение.\n"

        await self._send_respond(text, context)

    async def ref_queue_proc(self, context):
        """
        Implements the logic of the /reference queue command.
        """

        text = "/queue <@user|optional> \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['queue']} \n" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['queue']} "\
            f"уровня или выше \n" \
            f"* Может быть вызвана только в чате \n" \
            "\n" \
            "Описание: Добавляет пользователя в очередь сообщений медленного режима.\n"

        await self._send_respond(text, context)

    async def ref_unqueue_proc(self, context):
        """
        Implements the logic of the /reference unqueue command.
        """

        text = "/unqueue <@user|optional> \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['unqueue']} \n" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['unqueue']} "\
            f"уровня или выше \n"\
            f"* Может быть вызвана только в чате \n" \
            "\n" \
            "Описание: Удаляет пользователя из очереди сообщений медленного режима.\n"

        await self._send_respond(text, context)

    async def ref_info_proc(self, context):
        """
        Implements the logic of the /reference info command.
        """

        text = "/info <list_name> \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['info']} \n" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['info']} уровня или выше \n" \
            f"* Может быть вызвана только в лог-чате \n" \
            "\n" \
            "Описание: Выводит информацию о текущем состоянии "\
            "указанного списка объектов.\n" \
            "\n" \
            "Доступные аргументы: \n" \
            "* <list_name>: permission, setting, mark, kick, ban, mute, warn\n"

        await self._send_respond(text, context)

    async def ref_roll_proc(self, context):
        """
        Implements the logic of the /reference roll command.
        """

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
        """
        Implements the logic of the /reference say command.
        """

        text = "/say** <text> \n" \
            "* Доступные префиксы: ! или / \n" \
            f"* Псевдонимы команды: {ALIASES['say']} \n" \
            f"* Доступ для группы прав {PERMISSION_ACCESS['say']} уровня или выше \n" \
            f"* Может быть вызвана только в чате \n" \
            "\n" \
            "Описание: Отправляет сообщение от лица бота с указанным текстом.\n" \
            "\n" \
            "Доступные аргументы: \n" \
            "* <text>: Текст сообщения. Любой текст, "\
            "с учетом пробелов и спец. символов\n"

        await self._send_respond(text, context)
