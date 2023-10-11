"""
Initialization file for the local bot config module
"""

from .usr_config import (
    TOKEN,
    GROUP_ID,
    STAFF_ADMIN_ID,
    PREFIXES,
    QUEUE_TIME,
    PERMISSION_ACCESS,
    ALIASES,
    ALLOWED_DOMAIN,
    ALLOWED_URL,
    CRITICAL_DOMAIN,
    CRITICAL_URL,
    CURSE_WORDS
)
from .src_config import (
    TIME_TYPE,
    TIME_COEFFICIENT,
    PERMISSION_LVL,
    SETTINGS,
    EMOJI_NUMBERS
)

__all__ = (
    # user config variables
    "TOKEN",
    "GROUP_ID",
    "STAFF_ADMIN_ID",

    "PREFIXES",
    "QUEUE_TIME",
    "PERMISSION_ACCESS",
    "ALIASES",

    "ALLOWED_URL",
    "ALLOWED_DOMAIN",
    "CRITICAL_URL",
    "CRITICAL_DOMAIN",

    "CURSE_WORDS",

    # source config
    "TIME_TYPE",
    "TIME_COEFFICIENT",
    "PERMISSION_LVL",
    "SETTINGS",
    "EMOJI_NUMBERS"
)
