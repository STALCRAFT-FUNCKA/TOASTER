"""A file that describes the router class required to create custom event objects.
"""
import logging
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEvent
from .events import (
    BaseEvent,
    MessageEvent,
    ChatEvent,
    ButtonEvent
)

class Router(object):
    """A router class that creates custom events
    according to the type of raw event.

    Args:
        raw_event (Event): vk longpoll event.
        api (VkApi): vk api object.

    Returns:
        CustomEvent: Custom event
    """
    _logger = logging.getLogger("TOASTER")

    _event_blacklist = ()

    def _route(self, raw_event: dict, api: VkApi) -> BaseEvent:
        """The function determines the type of raw event,
        and then routes it to the desired custom event for subsequent redefinition.

        Args:
            raw_event (Event): vk longpoll event object.
            api (VkApi): vk api object.

        Returns:
            CustomEvent: Custom event object.
        """
        reason = None

        if raw_event.get("type") in self._event_blacklist:
            reason = "black-listed"

        if reason is not None:
            self._logger.warning(
                "Event <%s|%s> skipped. Reason: %s \n",
                raw_event.get("event_id"),
                raw_event.get("type"),
                reason
            )
            return None

        event_object = raw_event.get("object")

        if event_object is not None:
            if event_object["message"].get("action") is not None:
                return ChatEvent(raw_event, api)

            elif event_object.get("payload") is not None:
                return ButtonEvent(raw_event, api)

            else:
                return MessageEvent(raw_event, api)

        return None


    def __call__(self, vk_event: VkBotEvent, api: VkApi) -> BaseEvent:
        return self._route(vk_event.raw, api)
