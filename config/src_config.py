"""
File with source settings.
It is not recommended to change these settings.
"""

# Time type chars
TIME_TYPE = {
    'h': 'hour(s)',
    'd': 'day(s)',
    'm': 'month(s)',
}

# Time dimensions expressed in seconds
TIME_COEFFICIENT = {
    's': 1,
    'h': 1 * 60 * 60,
    'd': 1 * 60 * 60 * 24,
    'm': 1 * 60 * 60 * 24 * 31,
}

# Standard set of access rights levels
PERMISSION_LVL = {
    0: 'User',
    1: 'Moderator',
    2: 'Administrator',
}

# Standard settings that are initialized when a conversation is marked
SETTINGS = {
    'Allow_Picture': 1,
    'Allow_Video': 1,
    'Allow_Music': 1,
    'Allow_Links': 1,
    'Allow_Voice': 1,
    'Allow_Post': 1,
    'Allow_Votes': 1,
    'Allow_Files': 1,
    'Allow_Miniapp': 1,
    'Allow_Graffiti': 1,
    'Allow_Sticker': 1,
    'Allow_Reply': 1,
    'Filter_Curse': 0,
    'Slow_Mode': 0,
    'Account_Age': 0,
    'Hard_Mode': 0,
    'Need_PM': 0
}

# "Table" of matching numbers to be represented in the form of an emoji
EMOJI_NUMBERS = {
    1: '1️⃣',
    2: '2️⃣',
    3: '3️⃣',
    4: '4️⃣',
    5: '5️⃣',
    6: '6️⃣',
    7: '7️⃣',
    8: '8️⃣',
    9: '9️⃣',
    0: '0️⃣'
}
