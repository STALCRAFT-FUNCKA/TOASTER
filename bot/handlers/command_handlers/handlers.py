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

        api.messages.send(
            peer_id=event.peer_id,
            random_id=0,
            message=answer_text
        )
        
        return True



commands = {
    "test": TestCommand,
}
