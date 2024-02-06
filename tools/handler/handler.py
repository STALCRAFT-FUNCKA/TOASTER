from abc import ABC, abstractmethod
from vk_api import VkApi
from bot.event_factory import BaseEvent


class ABCHandler(ABC):
    """The basic unit of event processing.
    Responsible for specific conditions and events
    events that occurred in the conversation and those that remained in VK event.

    Args:
        event (BaseEvent): Modified VKBotLongpoll event.
        api (VkApi): VK API object.

    Returns:
        bool: Handling status.
            True - handler triggered
            False - handler skiped
    """
    @abstractmethod
    def _handle(self, event: BaseEvent, api: VkApi, args, kwargs) -> bool:
        """Handling a custom event that returns the result of processing.
        It is used within the framework of one specific action with a custom event.

        Args:
            event (BaseEvent): Modified VKBotLongpoll event.
            api (VkApi): VK API object.

        Returns:
            bool: Handling status. Returns True if was handled.
        """


    def __call__(self, event: BaseEvent, api: VkApi, *args, **kwargs) -> bool:
        """Calls the class as a function,
        handling the received input
        BaseEvent object.
        """
        return self._handle(event, api, args, kwargs)
