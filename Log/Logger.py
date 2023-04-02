import datetime
import json
import time

from vkbottle.bot import Bot, Message

from Config import GROUP, PERMISSION_LVL, TOKEN
from DataBase import DataBaseTools as DBtools

bot = Bot(token=TOKEN)


async def log_banned(message: Message, users_info, time_value, time_type):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) ' \
            f'заблокировал данного @id{users_info[0].id} ' \
            f'(пользователя) ({users_info[0].first_name} {users_info[0].last_name}) ' \
            f'на {time_value} {time_type}\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    forward = {
        'peer_id': message.peer_id,
        'conversation_message_ids': [message.reply_message.conversation_message_id],
    }
    forward = json.dumps(forward)
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        forward=forward,
        random_id=0
    )


async def log_banned_url(message: Message, users_info, time_value, time_type):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name})' \
            f' заблокировал ' \
            f'данного @id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name}) ' \
            f'на {time_value} {time_type}, используя ссылку\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_system_banned(message: Message, users_info, time_value, time_type, reason):
    LOG_PEER = DBtools.get_log_conversation()

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'Система заблокировала ' \
            f'данного @id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name}) ' \
            f'на {time_value} {time_type}\n' \
            f'Причина: {reason}\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_muted(message: Message, users_info, time_value, time_type):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]
    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) заглушил ' \
            f'данного @id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name}) ' \
            f'на {time_value} {time_type}\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    forward = {
        'peer_id': message.peer_id,
        'conversation_message_ids': [message.reply_message.conversation_message_id],
    }
    forward = json.dumps(forward)
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        forward=forward,
        random_id=0
    )


async def log_muted_url(message: Message, users_info, time_value, time_type):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) заглушил ' \
            f'данного @id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name}) ' \
            f'на {time_value} {time_type}, используя ссылку\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_system_muted(message: Message, users_info, time_value, time_type, reason):
    LOG_PEER = DBtools.get_log_conversation()

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'Система заглушила ' \
            f'данного @id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name}) ' \
            f'на {time_value} {time_type}\n' \
            f'Причина: {reason}\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_unmuted(message: Message, users_info):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) ' \
            f'разглушил ' \
            f'данного @id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name})\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    forward = {
        'peer_id': message.peer_id,
        'conversation_message_ids': [message.reply_message.conversation_message_id],
    }
    forward = json.dumps(forward)
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        forward=forward,
        random_id=0
    )


async def log_unmuted_url(message: Message, users_info):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) ' \
            f'разглушил ' \
            f'данного @id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name}), ' \
            f'используя ссылку\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_warned(message: Message, users_info, warn_count):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    epoch += (24 * 60 * 60 * 1)

    Moscow_tomorrow = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) выдал ' \
            f'предупреждение ' \
            f'@id{users_info[0].id} (пользователю) ({users_info[0].first_name} {users_info[0].last_name})\n' \
            f'Количество предупреждений: {warn_count}/3\n' \
            f'Предупреждения будут сняты: {Moscow_tomorrow}\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    forward = {
        'peer_id': message.peer_id,
        'conversation_message_ids': [message.reply_message.conversation_message_id],
    }
    forward = json.dumps(forward)
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        forward=forward,
        random_id=0
    )


async def log_warned_url(message: Message, users_info, warn_count):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    epoch += (24 * 60 * 60 * 1)

    Moscow_tomorrow = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) выдал ' \
            f'предупреждение ' \
            f'@id{users_info[0].id} (пользователю) ({users_info[0].first_name} {users_info[0].last_name}), ' \
            f'используя ссылку\n' \
            f'Количество предупреждений: {warn_count}/3\n' \
            f'Предупреждения будут сняты: {Moscow_tomorrow}\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_system_warned(message: Message, users_info, warn_count, reason):
    LOG_PEER = DBtools.get_log_conversation()

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    epoch += (24 * 60 * 60 * 1)

    Moscow_tomorrow = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'Система выдала ' \
            f'предупреждение ' \
            f'@id{users_info[0].id} (пользователю) ({users_info[0].first_name} {users_info[0].last_name})\n' \
            f'Количество предупреждений: {warn_count}/3\n' \
            f'Предупреждения будут сняты: {Moscow_tomorrow}\n' \
            f'Причина: {reason}\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    forward = {
        'peer_id': message.peer_id,
        'conversation_message_ids': [message.conversation_message_id],
    }
    forward = json.dumps(forward)
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        forward=forward,
        random_id=0
    )


async def log_unbanned(message: Message, users_info):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) ' \
            f'разблокировал ' \
            f'данного @id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name})\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    forward = {
        'peer_id': message.peer_id,
        'conversation_message_ids': [message.reply_message.conversation_message_id],
    }
    forward = json.dumps(forward)
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        forward=forward,
        random_id=0
    )


async def log_unbanned_url(message: Message, users_info):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) ' \
            f'разблокировал ' \
            f'данного @id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name}), ' \
            f'используя ссылку\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_unwarned(message: Message, users_info, warn_count):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) снял ' \
            f'предупреждение с ' \
            f'@id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name})\n' \
            f'Количество предупреждений: {warn_count}/3\n' \
            f'Предупреждения будут сняты через сутки\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    forward = {
        'peer_id': message.peer_id,
        'conversation_message_ids': [message.reply_message.conversation_message_id],
    }
    forward = json.dumps(forward)
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        forward=forward,
        random_id=0
    )


async def log_unwarned_url(message: Message, users_info, warn_count):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) снял ' \
            f'предупреждение с ' \
            f'@id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name}), ' \
            f'используя ссылку\n' \
            f'Количество предупреждений: {warn_count}/3\n' \
            f'Предупреждения будут сняты через сутки\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_deleted(message: Message):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) ' \
            f'удалил сообщения\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    if message.fwd_messages:
        forward = {
            'peer_id': message.peer_id,
            'conversation_message_ids': [msg.conversation_message_id for msg in message.fwd_messages],
        }

    else:
        forward = {
            'peer_id': message.peer_id,
            'conversation_message_ids': [message.reply_message.conversation_message_id],
        }

    forward = json.dumps(forward)
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        forward=forward,
        random_id=0
    )


async def log_log_conversation_changed(message: Message):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) ' \
            f'установил новую беседу в качестве лог-чата\n' \
            f'ID источника: {message.peer_id}\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_cooldown_changed(message: Message, cooldown):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) ' \
            f'установил новую задержку.\n' \
            f'Задержка: {cooldown} second(s)\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_permission_changed(message: Message, users_info, permission_lvl):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) ' \
            f'изменил группу прав для ' \
            f'данного @id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name}) ' \
            f'на {permission_lvl} уровень ({PERMISSION_LVL[str(permission_lvl)]})\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_permission_changed_url(message: Message, users_info, permission_lvl):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) ' \
            f'изменил группу прав для ' \
            f'данного @id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name}) ' \
            f'на {permission_lvl} уровень ({PERMISSION_LVL[str(permission_lvl)]}), ' \
            f'используя ссылку\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_setting_changed(message: Message, setting, value):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) ' \
            f'изменил настройку ' \
            f'{setting} на значение {value}\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_system_temp_ban_removed(peer_id, user_id):
    LOG_PEER = DBtools.get_log_conversation()

    users_info = await bot.api.users.get(user_id)

    conversations_info = await bot.api.messages.get_conversations_by_id(
        group_id=GROUP,
        peer_ids=peer_id
    )
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'Система сняла временную блокировку с ' \
            f'@id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name})\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_system_mute_removed(peer_id, user_id):
    LOG_PEER = DBtools.get_log_conversation()

    users_info = await bot.api.users.get(user_id)

    conversations_info = await bot.api.messages.get_conversations_by_id(
        group_id=GROUP,
        peer_ids=peer_id
    )
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'Система сняла временное заглушение с ' \
            f'@id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name})\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_system_warn_removed(peer_id, user_id):
    LOG_PEER = DBtools.get_log_conversation()

    users_info = await bot.api.users.get(user_id)

    conversations_info = await bot.api.messages.get_conversations_by_id(
        group_id=GROUP,
        peer_ids=peer_id
    )
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'Система сняла все предупреждения с ' \
            f'@id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name})\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_removed_from_queue(message: Message, user_info):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name})' \
            f'удалил из очереди задержки' \
            f'@id{user_info[0].id} (пользователя) ({user_info[0].first_name} {user_info[0].last_name})\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_removed_from_queue_url(message: Message, user_info):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    author_info = await bot.api.users.get(author_id)

    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    epoch = int(time.time())

    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset, name='МСК')

    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

    title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) ' \
            f'удалил из очереди задержки ' \
            f'@id{user_info[0].id} (пользователя) ({user_info[0].first_name} {user_info[0].last_name})' \
            f', используя ссылку\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_system_permission_changed(message: Message, users_info, permission_lvl):
    LOG_PEER = DBtools.get_log_conversation()

    if LOG_PEER != 0:
        conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
        conversations_name = conversations_info.items[0].chat_settings.title

        epoch = int(time.time())

        offset = datetime.timedelta(hours=3)
        tz = datetime.timezone(offset, name='МСК')

        Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

        title = f'Система ' \
                f'изменила группу прав для ' \
                f'данного @id{users_info[0].id} (пользователя) ({users_info[0].first_name} {users_info[0].last_name}) ' \
                f'на {permission_lvl} уровень ({PERMISSION_LVL[str(permission_lvl)]})\n' \
                f'Источник: {conversations_name}\n' \
                f'Время (МСК): {Moscow_time}'

        await bot.api.messages.send(
            group_id=GROUP,
            peer_id=LOG_PEER,
            message=title,
            random_id=0
        )


async def log_msg_copied(message: Message):
    LOG_PEER = DBtools.get_log_conversation()

    if LOG_PEER != 0:
        author_permission = DBtools.get_permission(message, message.from_id)
        author_id = message.from_id
        author_info = await bot.api.users.get(author_id)

        if author_permission == 1:
            author_permission = 'Модератор'

        elif author_permission == 2:
            author_permission = 'Администратор'

        conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
        conversations_name = conversations_info.items[0].chat_settings.title

        epoch = int(time.time())

        offset = datetime.timedelta(hours=3)
        tz = datetime.timezone(offset, name='МСК')

        Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

        title = f'@id{author_id} ({author_permission}) ({author_info[0].first_name} {author_info[0].last_name}) ' \
                f'скопировал сообщение\n ' \
                f'Источник: {conversations_name}\n' \
                f'Время (МСК): {Moscow_time}'
        forward = {
            'peer_id': message.peer_id,
            'conversation_message_ids': [message.reply_message.conversation_message_id],
        }
        forward = json.dumps(forward)
        await bot.api.messages.send(
            group_id=GROUP,
            peer_id=LOG_PEER,
            message=title,
            forward=forward,
            random_id=0
        )