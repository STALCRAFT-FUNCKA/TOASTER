from abc import ABC, abstractmethod


class ABCEvent(ABC):

    # Main event data
    user_id: int = None
    peer_id: int = None

    raw_type: int = None

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
