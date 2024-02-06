from vk_api import VkApi
from tools.handler import ABCHandler
from tools.keyboard import (
    Keyboard,
    Callback,
    ButtonColor
)
from bot.event_factory import MessageEvent



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

        answer_keyboard = (
            Keyboard(inline=True, one_time=False)
            .add_row()
            .add_button(
                Callback(
                    label="Позитив",
                    payload={
                        "button": "positive",
                        "call_action": "None"
                    }
                ),
                ButtonColor.POSITIVE
            )
            .add_button(
                Callback(
                    label="Негатив",
                    payload={
                        "button": "negative",
                        "call_action": "None"
                    }
                ),
                ButtonColor.NEGATIVE
            )
        )

        api.messages.send(
            peer_id=event.peer_id,
            random_id=0,
            message=answer_text,
            keyboard=answer_keyboard.json
        )

        return True



commands = {
    "test": TestCommand,
}
