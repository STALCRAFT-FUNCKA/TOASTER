"""
Главный файл настроек
"""

"""
Токен бота.
"""
# TODO: Вписать его способ получения в доку
TOKEN = 'vk1.a.zgY9PVhHltfqgBW-DGSbvizCe-pj3yqZyrSq3PDD-hRuRbIGALz2UN19tWaQRU8ANzSP12DPook-E9RrytgIG7k2wEIkUUDGOsCkFPq-PR_RmHyBCVthqdIg6I09K2WvRNTsQpifVF8-9-FKGWbrU87UFAEXp2aqh6LmOe5EqwMxbtOygx4yxC0I3k5sheMaOoM7r9hgOEdTAq8L3eeXAw'

"""
ID группы, на которой инициализирован бот.
"""
# TODO: Вписать его способ получения в доку
GROUP_ID = 218730916

"""
ID главного админа.
"""
# TODO: Вписать его назначение
STUFF_ADMIN_ID = 1

"""
------------------------------------------------------------------------------------------------------------------------
"""
"""
Время
"""
TIME_TYPE = {
    'h': 'hour(s)',
    'd': 'day(s)',
    'm': 'month(s)',
}

TIME_COEFFICENT = {
    'h': 1 * 60 * 60,
    'd': 1 * 60 * 60 * 24,
    'm': 1 * 60 * 60 * 24 * 31,
}

PERMISSION_LVL = {
    0: 'User',
    1: 'Moderator',
    2: 'Administrator',
}

# std settings
SETTINGS = {
    'Allow_Picture': False,
    'Allow_Video': False,
    'Allow_Music': False,
    'Allow_Voice': False,
    'Allow_Post': False,
    'Allow_Votes': False,
    'Allow_Files': False,
    'Allow_Miniapp': False,
    'Allow_Graffiti': False,
    'Allow_Sticker': False,
    'Allow_Reply': False,
}

ALIASES = {
    'reference': ['reference', 'справка'],
    # ----------------------------------
    'delete': ['delete', 'удалить'],
    'copy': ['copy', 'копировать'],
    # ----------------------------------
    'enroll': ['enroll', 'зарегистрировать'],
    'drop': ['drop', 'сбросить'],
    # ----------------------------------
    'enroll_log': ['enroll_log', 'зарегистрировать_лог'],
    'drop_log': ['drop_log', 'сбросить_лог'],
    # ----------------------------------
    'permission': ['permission', 'права'],
    # ----------------------------------
    'kick': ['kick', 'кик'],
    # ----------------------------------
    'ban': ['ban', 'бан'],
    'unban': ['unban', 'разбан'],
    # ----------------------------------
    'mute': ['mute', 'мут'],
    'unmute': ['unmute', 'размут'],
    # ----------------------------------
    'warn': ['warn', 'пред'],
    'unwarn': ['unwarn', 'разпред'],

}
