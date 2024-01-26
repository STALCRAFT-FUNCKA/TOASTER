from abc import ABC, abstractmethod


class ABCEvent(ABC):
    
    user_id:int = None
    peer_id:int = None
    
    @abstractmethod
    def handle(self):
        pass
    

class Command(ABCEvent):
    def handle(self):
        """
        docstring
        """
        pass
    

class Message(ABCEvent):
    def handle(self):
        """
        docstring
        """
        pass
    

class Factory(object):
    def __call__(self):
        pass
        