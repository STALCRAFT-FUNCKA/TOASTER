"""
File with user settings that can be changed painlessly and easily.
"""

import os

# Bot main token
TOKEN = os.getenv("TOASTER_TOKEN")

# Bot shell-group id
GROUP_ID = int(os.getenv("TOASTER_GROUPID"))

# Super-Admin id
STAFF_ADMIN_ID = int(os.getenv("TOASTER_STAFFADMID"))

# Prefixes that can accept commands
PREFIXES = ("!", "/")

# Slow mode delay in seconds
QUEUE_TIME = 30 * 60  # 30 minutes

# Access level for each command
PERMISSION_ACCESS = {
    "reference": 1,
    "mark": 2,
    "permission": 2,
    "terminate": 2,
    "kick": 1,
    "ban": 1,
    "unban": 1,
    "mute": 1,
    "unmute": 1,
    "warn": 1,
    "unwarn": 1,
    "delete": 1,
    "copy": 1,
    "setting": 2,
    "queue": 1,
    "unqueue": 1,
    "info": 1,
    "say": 2,
    "roll": 0,
    "hate_soloma": 1
}

# Aliases that can accept commands
ALIASES = {
    'reference': ('reference', 'ref', 'справка'),
    # ----------------------------------
    'delete': ('delete', 'del', 'удалить'),
    'copy': ('copy', 'копировать'),
    # ----------------------------------
    'mark': ('mark', 'метка'),
    # ----------------------------------
    'permission': ('permission', 'perm', 'права'),
    # ----------------------------------
    'terminate': ('terminate', 'term', 'терминировать'),
    # ----------------------------------
    'kick': ('kick', 'кик'),
    # ----------------------------------
    'ban': ('ban', 'бан'),
    'unban': ('unban', 'разбан'),
    # ----------------------------------
    'mute': ('mute', 'мут'),
    'unmute': ('unmute', 'размут'),
    # ----------------------------------
    'warn': ('warn', 'пред'),
    'unwarn': ('unwarn', 'разпред'),
    # ----------------------------------
    'setting': ('setting', 'set', 'настройка'),
    # ----------------------------------
    'queue': ('queue', 'очередь'),
    'unqueue': ('unqueue', 'разочередить'),
    # ----------------------------------
    'info': ('info', 'информация'),
    # ----------------------------------
    'roll': ('roll', 'прокрутить'),
    'say': ('say', 'сказать'),
    'hate_soloma': ('hate_soloma', 'зачмырить_солому')
}

# URL filter settings
# Always allowed urls
ALLOWED_URL = (
    'discord.com/invite/stalcraft',
    'vk.com/stalcraft_official',
    'vk.com/exbo_official',
    't.me/stalcraft',
    'www.tiktok.com/@stalcraft_official',
    'www.youtube.com/EXBO_official',
    'store.steampowered.com/toaster_app/1818450/STALCRAFT',
    'www.twitch.tv/exbo_official',
    'disk.yandex.ru/d/2LNeePtemDTsNg'
)

# Always allowed domains
ALLOWED_DOMAIN = (
    'stalcraft.net',
    'exbo.net',
    'support.exbo.net',
    'forum.exbo.net',
    'stalcraftmap.net',
    'stalcraft.wiki',
    'stalcalc.net'
)

# Always forbidden urls
CRITICAL_URL = ()

# Always forbidden domains
CRITICAL_DOMAIN = (
    'yougame.biz',
    'funpay.com',
    'stalcase.ru',
    'www.pwn.ac',
    'scmarket.ru',
    'cubedrop.ru',
    'www.unknowncheats.me',
    'stalcraftgurus.mysellix.io',
    'ezyhack.ru',
    'mir-hack.ru',
    'gamexworld.com',
    'trainer-engine.ru',
    'www.game-rpg.ru,'
    'plati.market',
    'stolcraft.online',
    'cheatermad.com',
)

# Curse words from curse filter
# Use only this pattern ( ' word ' )
CURSE_WORDS = (
    ' чр ',
    ' фп ',
    ' чит ',
    ' читы ',
    ' fp ',
    ' фан пей ',
    ' фан пэй ',
)
