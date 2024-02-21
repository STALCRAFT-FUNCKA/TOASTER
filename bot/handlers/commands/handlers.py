from vk_api import VkApi
from tools.handler import ABCHandler
from bot.event_factory import MessageEvent
from .keyboards import (
    TestCommandKbd,
    MarkCommandKbd,
)



class TestCommand(ABCHandler):
    """Test command.
    Sends test content to the chat where the command was called:
        Message
        Attachments
        Keyboard
        e.t.c
    """
    COMMAND_NAME = "test"

    def _handle(self, event: MessageEvent, api: VkApi, args, kwargs) -> bool:
        answer_text = f"Вызвана комманда <{self.COMMAND_NAME}> " \
                      f"с аргументами {kwargs.get('argument_list')}."

        api.messages.send(
            peer_id=event.peer_id,
            random_id=0,
            message=answer_text,
            keyboard=TestCommandKbd.json
        )

        return True



class MarkCommand(ABCHandler):
    """Mark command.
    Initializes conversation marking process.
    Allows:
        - To mark conversation as "CHAT" or "LOG".
        - Update the data about conversation.
        - Delete conversation mark.
    """
    COMMAND_NAME = "mark"

    def _handle(self, event: MessageEvent, api: VkApi, args, kwargs) -> bool:
        answer_text = "⚠️ Вы хотите пометить новую беседу? \n\n" \
        "Выберите необходимое дествие из меню ниже:"

        api.messages.send(
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
