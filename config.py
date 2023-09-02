"""
Главный файл настроек
"""

"""
Токен бота.
Сообщество > управление > настройки > работа с API > создать ключ
Указать ВСЕ галочки при выдаче доступов.
"""
TOKEN = 'vk1.a.zgY9PVhHltfqgBW-DGSbvizCe-pj3yqZyrSq3PDD-hRuRbIGALz2UN19tWaQRU8ANzSP12DPook-E9RrytgIG7k2wEIkUUDGOsCkFPq-PR_RmHyBCVthqdIg6I09K2WvRNTsQpifVF8-9-FKGWbrU87UFAEXp2aqh6LmOe5EqwMxbtOygx4yxC0I3k5sheMaOoM7r9hgOEdTAq8L3eeXAw'

"""
ID группы, на которой инициализирован бот.
Ссылку на сообщество можно найти в строке ссылки браузера. Ссылку указывать в формате vk.com/community_name
ID группы: Сообщество > управление > настройки
"""

GROUP_ID = 218730916
GROUP_URL = "vk.com/toaster"

"""
ID главного админа.
Важно! Здесь должно быть именно численное ID.
ID стаф-админа определяет главного администратора с исключительными правами.
Он может ВСЕ, без использования VK-admin.
Так же будет указываться ссылка на него в репонда, чтобы помогать пользователям.
"""
STUFF_ADMIN_ID = 1

"""
------------------------------------------------------------------------------------------------------------------------
"""
"""
Префиксы вызова команды.
Для того, чтобы команда вызывалась по пользовательскому префиксу - добавьте его в кортеж.
Поле не должно быть пустым.
"""
PREFIXES = ("!", "/")

"""
Настройка задержки в беседах. 
При включенном в беседе медленном режиме задержка будет составлять время, указанное в значении в секундах.
Время статично применяется для всех бесед с функцией медленного режима.
"""
QUEUE_TIME = 30 * 60  # 30 minutes

"""
Полные название времен.
Не рекомендуется к изменению.
"""
TIME_TYPE = {
    'h': 'hour(s)',
    'd': 'day(s)',
    'm': 'month(s)',
}
"""
Коэффициенты времени.
Не рекомендуется к изменению
"""
TIME_COEFFICENT = {
    'h': 1 * 60 * 60,
    'd': 1 * 60 * 60 * 24,
    'm': 1 * 60 * 60 * 24 * 31,
}

"""
При изменении роли достаточно изменить нужное значение.
Значение слева от знака ":" трогать не рекомендуется. Если же, вы нарочно не хотите что-то сломать.
Значение не должно быть пустым.
Данная настройка отвечает за название прав по уровню доступа.
"""
PERMISSION_LVL = {
    0: 'User',
    1: 'Moderator',
    2: 'Administrator',
}

PERMISSION_ACCESS = {
    "reference": 0,
    "enroll": 0,
    "drop": 0,
    "enroll_log": 0,
    "drop_log": 0,
    "terminate": 0,
    "kick": 0,
    "unban": 0,
    "mute": 0,
    "unmute": 0,
    "warn": 0,
    "unwarn": 0,
    "delete": 0,
    "copy": 0,
    "setting": 0,
}

"""
При изменении настроек беседы достаточно изменить нужное значение на True or False.
Значение слева от знака ":" трогать не рекомендуется. Если же, вы нарочно не хотите что-то сломать.
Значение не должно быть пустым.
Данная настройка определяет по стандарту запрещенные вещи\сущности в беседе.
"""
SETTINGS = {
    'Allow_Picture': False,
    'Allow_Video': False,
    'Allow_Music': False,
    'Allow_Links': False,
    'Allow_Voice': False,
    'Allow_Post': False,
    'Allow_Votes': False,
    'Allow_Files': False,
    'Allow_Miniapp': False,
    'Allow_Graffiti': False,
    'Allow_Sticker': False,
    'Allow_Reply': False,
    'Filter_Curse': False,
    'Slow_Mode': False,
    'Account_Age': False,
    'Hard_Mode': False
}

"""
При изменении псевдонимов команды достаточно добавить\удалить нужное значение в кортеж.
Значение слева от знака ":" трогать не рекомендуется. Если же, вы нарочно не хотите что-то сломать.
Кортеж с псевдонимами не должен быть оставлен пустым. Чтобы команда работала - нужен хоть один псевдоним.
Данная настройка определяет, при помощи какого имени комбинацией / + <cmd_name> можно исполнить действие.
"""
ALIASES = {
    'reference': ('reference', 'справка'),
    # ----------------------------------
    'delete': ('delete', 'удалить'),
    'copy': ('copy', 'копировать'),
    # ----------------------------------
    'enroll': ('enroll', 'зарегистрировать'),
    'drop': ('drop', 'сбросить'),
    # ----------------------------------
    'enroll_log': ('enroll_log', 'зарегистрировать_лог'),
    'drop_log': ('drop_log', 'сбросить_лог'),
    # ----------------------------------
    'permission': ('permission', 'права'),
    # ----------------------------------
    'terminate': ('terminate', 'терминировать'),
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
    'setting': ('setting', 'настройка'),
}

"""
Разрешенные и запрещенные ссылки.
В режиме обычного модерирования: Выдается наказание только за ссылки из раздела CRITICAL
В режиме Hard модерирования: Выдается наказание за ссылки из раздела CRITICAL. За все остальные ссылки - следует
предупреждение. Исключением выступают ссылки из раздела ALLOWED - за них наказание не выдается.
Внимание: ССЫЛКИ УКАЗЫВАТЬ БЕЗ ПРОТОКОЛА HTTP (HTTPS)
"""

# Разрешены всегда
ALLOWED_URL = (
    'discord.com/invite/stalcraft',
    'vk.com/stalcraft_official',
    'vk.com/exbo_official',
    't.me/stalcraft',
    'www.tiktok.com/@stalcraft_official',
    'www.youtube.com/EXBO_official',
    'store.steampowered.com/app/1818450/STALCRAFT',
    'www.twitch.tv/exbo_official',
    'disk.yandex.ru/d/2LNeePtemDTsNg'
)

ALLOWED_DOMAIN = (
    'stalcraft.net',
    'exbo.net',
    'support.exbo.net',
    'forum.exbo.net',
    'stalcraftmap.net',
    'stalcraft.wiki',
    'stalcalc.net'
)

# Мут. Запрещены всегда.
CRITICAL_URL = ()

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

"""
Curse filter
"""
CURSE_WORDS = (
    ' чр ',
    ' фп ',
    ' чит ',
    ' читы ',
    ' fp ',
    ' фан пей ',
    ' фан пэй ',
)
