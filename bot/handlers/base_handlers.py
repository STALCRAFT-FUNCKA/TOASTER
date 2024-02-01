"""File describing abstract handler objects.
"""
import logging
from abc import ABC, abstractmethod
from vk_api import VkApi
from ..event_factory import MessageEvent


class ABCMainHandler(ABC):
    """Abstract main handler class.
    The main handler acts as a “machine” that accepts input
    object of a custom event, after which it applies everything one by one
    handlers available to her for this event. If at least one event is triggered -
    the main handler will stop its work and determine the event as handled.

    Args:
        event (BaseEvent): Modified VKBotLongpoll event.
        
    Returns:
        bool: Handling status. Returns True if was handled.
    """
    # logger object
    __logger = logging.getLogger("TOASTER")

    # VK api object
    # It is necessary for receipt
    # an additional data of the events
    # and making actions with it
    __api: VkApi = None

    def __init__(self, api: VkApi):
        self.__api = api


    @abstractmethod
    def _check(self, event: MessageEvent) -> bool:
        """The need to check conditions 
        (existence fields, text form).
        
        Returns:
            bool: Checking result.
        """


    @abstractmethod
    def _handle(self, event: MessageEvent, args, kwargs) -> bool:
        """Handle a custom event, returning the processing result.
        Applies all handlers one by one to the custom event object.

        Args:
            event (BaseEvent): Modified VKBotLongpoll event.

        Returns:
            bool: Handling status. Returns True if was handled.
        """


    def __call__(self, event: MessageEvent, *args, **kwargs) -> bool:
        """Calls the class as a function,
        handling the received input
        BaseEvent object.
        """
        if self.__api is not None:
            if self._check(event):
                return self._handle(event, args, kwargs)
        else:
            self.__logger.error(
                "Unable to handle event <%s|%s}>. "
                "Handler <%s> does not have an API object.",
                event.event_id,
                event.event_type,
                self.__class__.__name__
            )

        return False


    @property
    def api(self):
        """Returns the VKontakte API object from the parent class.

        Returns:
            VkApi: vk api object.
        """
        return self.__api


    @property
    def logger(self):
        """Returns the logger object from the parent class.

        Returns:
            Logger: logger object.
        """
        return self.__logger



class ABCHandler(ABC):
    """The basic unit of event processing.
    Responsible for specific conditions and events
    events that occurred in the conversation and those that remained in VK event.

    Args:
        event (BaseEvent): Modified VKBotLongpoll event.
        api (VkApi): VK API object.

    Returns:
        bool: Handling status.
    """
    @abstractmethod
    def _handle(self, event: MessageEvent, api: VkApi, args, kwargs) -> bool:
        """Handling a custom event that returns the result of processing.
        It is used within the framework of one specific action with a custom event.

        Args:
            event (BaseEvent): Modified VKBotLongpoll event.
            api (VkApi): VK API object.

        Returns:
            bool: Handling status. Returns True if was handled.
        """


    def __call__(self, event: MessageEvent, api: VkApi, *args, **kwargs) -> bool:
        """Calls the class as a function,
        handling the received input
        BaseEvent object.
        """
        return self._handle(event, api, args, kwargs)
