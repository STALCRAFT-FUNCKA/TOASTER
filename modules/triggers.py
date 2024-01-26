"""
A module that provides a bot with the necessary set of processing of the message event, to obtain
information about the content of certain data related to the event.
"""

from abc import (
    ABC,
    abstractmethod
)

# TODO: Realise abstract trigger class
# Позже этот класс должен не только содержать в себе функцию обработки
# Но и функцию\данные, содержащие информацию о методе, времени и типе наказания
# Триггреры - это определения нарушения и формирование наказания за эти нарушения

class ABCTrigger(ABC):
    """_summary_

    Args:
        event (any): _description_

    Returns:
        bool: _description_
    """
    @abstractmethod
    def handler(self, event: any) -> bool:
        """_summary_

        Args:
            event (any): _description_

        Returns:
            bool: _description_
        """
        return False

    def __call__(self, event: any) -> bool:
        """_summary_
        """
        return self.handler(event)
