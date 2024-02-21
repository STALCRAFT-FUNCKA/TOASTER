"""A file that describes the router class required to create custom event objects.
"""
import logging
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEvent
from tools.event import (
    BaseEvent,
    MessageEvent,
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

    _routes = {
        "message_new": MessageEvent,
        "message_event": ButtonEvent
    }

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
        if raw_event.get("type") not in self._routes:
            reason = "missing route"

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

        return self._routes[raw_event.get("type")](raw_event, api)


    def __call__(self, vk_event: VkBotEvent, api: VkApi) -> BaseEvent:
        return self._route(vk_event.raw, api)
