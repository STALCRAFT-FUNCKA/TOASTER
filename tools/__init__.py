"""A module of tools designed to quickly
and convenient creation of VK API objects and bot systems.
"""
from .singletone import MetaSingleton
from .time import (
    timestamp,
    msk_now,
    msk_delta
)


__all__ = (
    "MetaSingleton",
    "timestamp",
    "msk_now",
    "msk_delta"
)
