"""
This file contains a description of the fun processor classes.
A processor is an object that has a certain semantic set of methods
that execute the basic logic of actions inside the bot. In other words,
the logic of filters, commands, handlers, etc.
"""

from singltone import MetaSingleton
from .core import StdProcessor


class FunProcessor(StdProcessor, metaclass=MetaSingleton):
    """
    Implements basic methods that perform specific actions on the command context.
    """

    async def fun_roll_proc(self, context, log=True, respond=True):
        """
        Implements the logic of the /roll command.
        """

        context["initiator_lvl"] = self._get_initiator_lvl(context)

        if respond:
            text = "Кости брошены!\n"
            await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        result_text = (
            f"{context.get('initiator_nametag')} выбивает число "
            f"({context.get('down_border')}-{context.get('up_border')}):"
            f"{context.get('result')}"
        )

        await self.bot.api.messages.send(
            chat_id=context.get("chat_id"),
            message=result_text,
            random_id=0
        )

    async def fun_say_proc(self, context, log=True, respond=True):
        """
        Implements the logic of the /say command.
        """

        context["initiator_lvl"] = self._get_initiator_lvl(context)

        if respond:
            text = "Сообщение отправлено.\n"
            await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        await self.bot.api.messages.send(
            chat_id=context.get("chat_id"),
            message=context.get("say_text"),
            random_id=0
        )

    async def fun_hate_soloma_proc(self, context, log=True, respond=True):
        """
        Implements the logic of the /hate_soloma command.
        """

        context["initiator_lvl"] = self._get_initiator_lvl(context)

        if respond:
            text = "Солома зачмырён.\n"
            await self._send_respond(text, context)
        if log:
            await self._send_log(context)

        text = "СОЛОМА ТЫ ТАКОЙ ЛОХ!!!"

        await self.bot.api.messages.send(
            chat_id=context.get("chat_id"),
            message=text,
            random_id=0
        )
