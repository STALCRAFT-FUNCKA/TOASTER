from vk_api import VkApi
from tools.handler import ABCHandler
from tools.event import ButtonEvent
from tools.keyboard import SnackbarAnswer
from db import DataBase


class BaseAction(ABCHandler):
    """Base action handler class.
    """
    def __init__(self, db: DataBase, api: VkApi):
        self.db = db
        self.api = api


    def snackbar(self, event: ButtonEvent, text: str):
        """Sends a snackbar to the user.

        Args:
            event (ButtonEvent): VK button_pressed custom event.
            text (str): Sncakbar text.
        """
        self.api.messages.sendMessageEventAnswer(
            event_id=event.button_event_id,
            user_id=event.from_id,
            peer_id=event.peer_id,
            event_data=SnackbarAnswer(text).data
        )


    def log(self):
        """Sends a log of command execution
        in log-convs.
        """
        # TODO: write me