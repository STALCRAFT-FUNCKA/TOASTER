import json
from vk_api import VkApi
from ..base_handlers import ABCHandler
from ...event_factory import MessageEvent


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

        answer_keyboard = {
            "inline": True,
            "buttons": [
                [
                    {
                        "action":{
                            "type": "callback",
                            "payload": {
                                "keyboard_name": "test",
                                "button": "Test1"
                            },
                            "label": "Test1",
                        },
                        "color": "positive"
                    },
                    {
                        "action":{
                            "type": "callback",
                            "payload": {
                                "keyboard_name": "test",
                                "button": "Test2"
                            },
                            "label": "Test2",
                        },
                        "color": "negative"
                    },
                ]
            ]
        }
        api.messages.send(
            peer_id=event.peer_id,
            random_id=0,
            message=answer_text,
            keyboard=json.dumps(answer_keyboard)
        )

        return True



commands = {
    "test": TestCommand,
}
