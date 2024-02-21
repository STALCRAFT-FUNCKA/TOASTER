from tools.handler import ABCHandlingHub
from bot.event_factory import MessageEvent
from .handlers import commandlist


class CommandHandler(ABCHandlingHub):
    """Event handler class that recognizes commands
    in the message and executing attached to each command
    actions.
    """
    # Command prefixes: /test or !test
    COMMAND_PREFIX: tuple = ("!", "/")

    def _check(self, event: MessageEvent) -> bool:
        text: str = event.text

        if text is None:
            return False

        return text.startswith(self.COMMAND_PREFIX)


    def _handle(self, event: MessageEvent, args, kwargs) -> bool:
        command_text: str = event.text
        command_text_wo_prefix: str = command_text[1:]

        #command arguments
        arguments: list = command_text_wo_prefix.split(" ")
        #command name
        command: str = arguments.pop(0)

        selected = commandlist.get(command, None)

        if selected is None:
            super().logger.info(
                "Could not recognize command <%s>",
                command
            )
            return False

        selected = selected()
        return selected(event, super().api, argument_list=arguments)
