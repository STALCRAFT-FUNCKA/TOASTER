from tools.handler import ABCHandlingHub
from tools.event import MessageEvent
from db import DataBase
import config
from .handlers import commandlist


class CommandHandler(ABCHandlingHub):
    """Event handler class that recognizes commands
    in the message and executing attached to each command
    actions.
    """
    db = DataBase("toaster")

    def _check(self, event: MessageEvent) -> bool:
        text: str = event.text

        if text is None:
            return False

        return text.startswith(config.COMMAND_PREFIXES)


    def _handle(self, event: MessageEvent, kwargs) -> bool:
        command_text: str = event.text
        command_text_wo_prefix: str = command_text[1:]

        #command arguments
        arguments: list = command_text_wo_prefix.split(" ")[0:config.MAX_COMMAND_ARG_COUNT]
        #command name
        command: str = arguments.pop(0)

        selected = commandlist.get(command)

        if selected is None:
            super().logger.info(
                "Could not recognize command <%s>",
                command
            )
            return False

        selected = selected(self.db, super().api)

        user_lvl = self.__get_userlvl(event)
        if selected.permission <= user_lvl:
            return selected(event, argument_list=arguments)

        return False


    def __get_userlvl(self, event: MessageEvent) -> int:
        if event.from_id == config.STAFF_ADMIN_ID:
            return 2

        user_lvl = self.db.permissions.select(
            fields=("user_permission",),
            conv_id=event.peer_id
        )

        if bool(user_lvl):
            return int(user_lvl[0][0])

        return 0
        