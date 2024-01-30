"""
A module that provides a router for VK longpoll events
and custom events that are created based on them in the router.
"""
from .router import Router
from .events import CustomEvent

__all__ = (
    "Router",
    "CustomEvent"
)
