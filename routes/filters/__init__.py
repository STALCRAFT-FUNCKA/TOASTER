"""
File initializing the local filtres module.
"""

from .chat.age import bl as age_filter
from .chat.curse import bl as curse_filter
from .chat.forbidden import bl as forbidden_filter
from .chat.mute import bl as mute_filter
from .chat.queue import bl as queue_filter
from .chat.url import bl as url_filter
from .chat.pm import bl as pm_filter

__all__ = (
    "age_filter",
    "curse_filter",
    "forbidden_filter",
    "mute_filter",
    "queue_filter",
    "url_filter",
    "pm_filter"
)
