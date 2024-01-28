from abc import ABC, abstractmethod
from vk_api import VkApi


class ABCEvent(ABC):

    _api: VkApi = None
    
    raw_type: int = None

    # Main event data
    user_id: int = None
    peer_id: int = None

    @abstractmethod
    def handle(self):
        pass


class CommandCall(ABCEvent):
    def handle(self):
        """
        docstring
        """
        pass


class MessageSend(ABCEvent):
    def handle(self):
        """
        docstring
        """
        pass


class ButtonPreess(ABCEvent):
    def handle(self):
        """
        docstring
        """
        pass
