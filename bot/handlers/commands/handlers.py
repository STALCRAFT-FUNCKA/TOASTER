from tools.event import MessageEvent
from .base import BaseCommand
from .keyboards import (
    TestCommandKbd,
    MarkCommandKbd,
)


class TestCommand(BaseCommand):
    """Test command.
    Sends test content to the chat where the command was called:
        Message
        Attachments
        Keyboard
        e.t.c
    """
    __permission_lvl = 2
    COMMAND_NAME = "test"

    def _handle(self, event: MessageEvent, kwargs) -> bool:
        answer_text = f"Вызвана комманда <{self.COMMAND_NAME}> " \
                      f"с аргументами {kwargs.get('argument_list')}."

        self.api.messages.send(
            peer_id=event.peer_id,
            random_id=0,
            message=answer_text,
            keyboard=TestCommandKbd.json
        )

        return True



class MarkCommand(BaseCommand):
    """Mark command.
    Initializes conversation marking process.
    Allows:
        - To mark conversation as "CHAT" or "LOG".
        - Update the data about conversation.
        - Delete conversation mark.
    """
    __permission_lvl = 2
    COMMAND_NAME = "mark"

    def _handle(self, event: MessageEvent, kwargs) -> bool:
        answer_text = "⚠️ Вы хотите пометить новую беседу? \n\n" \
        "Выберите необходимое дествие из меню ниже:"

        self.api.messages.send(
            peer_id=event.peer_id,
            random_id=0,
            message=answer_text,
            keyboard=MarkCommandKbd.json
        )

        return True




commandlist = {
    "test": TestCommand,
    "mark": MarkCommand
}
