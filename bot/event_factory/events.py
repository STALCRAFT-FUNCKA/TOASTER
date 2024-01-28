from abc import ABC, abstractmethod
from vk_api import VkApi
from vk_api.longpoll import Event


class ABCCustomEvent(ABC):
    """_summary_
    """
    # VK api object
    # It is necessary for receipt
    # an additional data of the events
    # and making actions with it
    _api: VkApi = None

    raw_type: int = None

    # Main event data
    user_id: int = None
    peer_id: int = None
    chat_id: int = None
    tamestamp: str = None

    def __init__(self, raw_event: Event, api: VkApi = None):
        self._api = api

        self.raw_type = raw_event.type

        self.user_id = raw_event.user_id
        self.peer_id = raw_event.peer_id
        self.chat_id = raw_event.chat_id
        self.tamestamp = str(raw_event.datetime)

    def _get_additionals(self):
        if self._api is not None:
            pass
            # TODO: get additional data like full person name
        else:
            pass
            # TODO: log warning

    def dispose_event(self):
        pass

    @abstractmethod
    def handle(self):
        """_summary_
        """
        pass


class CommandCall(ABCCustomEvent):
    def handle(self):
        pass


class MessageSend(ABCCustomEvent):
    def handle(self):
        pass


class ButtonPreess(ABCCustomEvent):
    def handle(self):
        pass
