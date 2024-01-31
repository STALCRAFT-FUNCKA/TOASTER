"""A module that provides a router for VK longpoll events
and custom events that are created based on them in the router.
"""
from .router import Router
from .events import (
    BaseEvent,
    MessageEvent
)

__all__ = (
    "Router",
    "BaseEvent",
    "MessageEvent"
)
