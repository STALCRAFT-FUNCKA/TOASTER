"""
A file that describes the router class required to create custom event objects.
"""
import logging
from vk_api import VkApi
from vk_api.longpoll import Event, VkEventType
from .events import CustomEvent, MessageEvent


class Router(object):
    """
    A router class that creates custom events
    according to the type of raw event.

    Args:
        raw_event (Event): vk longpoll event.
        api (VkApi): vk api object.

    Returns:
        CustomEvent: Custom event
    """
    _logger = logging.getLogger("TOASTER")

    _event_blacklist = (
        VkEventType.USER_TYPING,
        VkEventType.USER_TYPING_IN_CHAT
    )

    _routes = {
        VkEventType.MESSAGE_NEW: MessageEvent,
        VkEventType.MESSAGE_EDIT: MessageEvent
    }


    def _route(self, raw_event: Event, api: VkApi) -> CustomEvent:
        """
        The function determines the type of raw event,
        and then routes it to the desired custom event for subsequent redefinition.

        Args:
            raw_event (Event): vk longpoll event object.
            api (VkApi): vk api object.

        Returns:
            CustomEvent: Custom event object.
        """
        reason = None
        if raw_event.type not in self._routes:
            reason = "missing route"

        if raw_event.type in self._event_blacklist:
            reason = "black-listed"

        if reason is not None:
            self._logger.warning(
                "Event %s skipped. Reason: %s", raw_event.type, reason
            )
            return None

        return self._routes[raw_event.type](raw_event, api)


    def __call__(self, raw_event: Event, api: VkApi) -> CustomEvent:
        return self._route(raw_event, api)
