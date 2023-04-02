"""
Bot main token
"""

TOKEN = ''
"""
Master group id
"""
GROUP = 0

"""
Moderation content
"""
TIME_TYPE = {
    'h': 'hour(s)',
    'd': 'day(s)',
    'm': 'month(s)',
    'p': 'permanent'
}

PERMISSION_LVL = {
    '0': 'User',
    '1': 'Moderator',
    '2': 'Administrator',
    '3': 'Operator'
}

SETTINGS = [
    'Allow_Picture',
    'Allow_Video',
    'Allow_Music',
    'Allow_Voice',
    'Allow_Post',
    'Allow_Votes',
    'Allow_Files',
    'Allow_Miniapp',
    'Allow_Graffiti',
    'Allow_Sticker',
    'Allow_Reply',
    'Allow_AgeCheck',
    'Allow_URLCheck'
]

ALIASES = {
    'ban': ['ban', 'Ban'],
    'ban_url': ['ban_url', 'Ban_url'],

    'unban': ['Unban', 'unban'],
    'unban_url': ['Unban_url', 'unban_url'],

    'warn': ['warn', 'Warn'],
    'warn_url': ['warn_url', 'Warn_url'],

    'unwarn': ['unwarn', 'Unwarn'],
    'unwarn_url': ['unwarn_url', 'Unwarn_url'],

    'delete': ['delete', 'Delete'],
    'reference': ['reference', 'Reference'],
    'set_cooldown': ['set_cooldown', 'Set_cooldown'],
    'set_log_conversation': ['set_log_conversation', 'Set_log_conversation'],
    'change_setting': ['change_setting', 'Change_setting'],
    'msg_copy': ['msg_copy', 'Msg_copy'],

    'set_permission': ['set_permission', 'Set_permission'],
    'set_permission_url': ['set_permission_url', 'Set_permission_url'],
    'get_permission': ['get_permission', 'Get_permission'],

    'mute': ['mute', 'Mute'],
    'mute_url': ['mute_url', 'Mute_url'],

    'unmute': ['unmute', 'Unmute'],
    'unmute_url': ['unmute_url', 'Unmute_url'],

    'remove_from_queue': ['remove_from_queue', 'Remove_from_queue'],
    'remove_from_queue_url': ['remove_from_queue_url', 'Remove_from_queue_url']

}

STUFF_ADMIN = 0
