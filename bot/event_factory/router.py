import logging
from vk_api import VkApi
from vk_api.longpoll import Event, VkEventType
from .events import CustomEvent, MessageEvent


class Router(object):
    _logger = logging.getLogger("TOASTER")

    _event_blacklist = (
        VkEventType.USER_TYPING,
        VkEventType.USER_TYPING_IN_CHAT
    )

    _routes = {
        VkEventType.MESSAGE_NEW: MessageEvent,
        VkEventType.MESSAGE_EDIT: MessageEvent
    }

    def route(self, raw_event: Event, api: VkApi) -> CustomEvent:
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
        return self.route(raw_event, api)
