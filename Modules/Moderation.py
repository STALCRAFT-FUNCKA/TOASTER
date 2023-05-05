import datetime
import time

from vkbottle.bot import Bot, BotLabeler, Message
from typing import Tuple
from Config import TIME_TYPE, ALIASES, TOKEN, SETTINGS, GROUP, STUFF_ADMIN
from Log import Logger as ol
from Rules.CustomRules import (
    HandleCommand,
    PermissionAccess,
    HandleRepliedMessages,
    PermissionIgnore,
    HandleLogConversation
)
from urlextract import URLExtract
from DataBase import DataBaseTools as DBtools

bot = Bot(token=TOKEN)
bl = BotLabeler()


@bl.chat_message(
    HandleCommand(ALIASES['reference'], ['!', '/'], 0),
    HandleLogConversation(True),
    PermissionAccess(1),
    HandleRepliedMessages(False)
)
async def reference(message: Message):
    url = 'https://github.com/Oidaho/FUNCKA-BOT/blob/master/README.md'

    title = f'Перейдя по этой ссылке, вы сможете найти документацию на GitHub:\n {url}'
    await message.answer(title)


@bl.chat_message(
    HandleCommand(ALIASES['ban'], ['!', '/'], 2),
    HandleLogConversation(False),
    PermissionAccess(1),
    PermissionIgnore(1),
    HandleRepliedMessages(True)
)
async def ban(message: Message, args: Tuple[str]):
    if not message.fwd_messages:
        ban_users_info = await bot.api.users.get(message.reply_message.from_id)
        if ban_users_info:
            offset = datetime.timedelta(hours=3)
            tz = datetime.timezone(offset, name='МСК')

            time_value = args[0]
            time_type = TIME_TYPE[args[1]]

            if args[1] == 'p':
                time_value = ''
                epoch = '--'

            elif args[1] == 'm':
                if int(time_value) < 0:
                    time_value = '1'
                if int(time_value) > 12:
                    time_value = '12'
                epoch = int(time.time()) + (31 * 24 * 60 * 60 * int(time_value))

            elif args[1] == 'd':
                if int(time_value) < 0:
                    time_value = '1'
                if int(time_value) > 31:
                    time_value = '31'
                epoch = int(time.time()) + (24 * 60 * 60 * int(time_value))

            elif args[1] == 'h':
                if int(time_value) < 0:
                    time_value = '1'
                if int(time_value) > 24:
                    time_value = '24'
                epoch = int(time.time()) + (60 * 60 * int(time_value))

            else:
                time_value = '1'
                time_type = TIME_TYPE['h']
                epoch = int(time.time()) + (60 * 60 * 1)

            if epoch == '--':
                Moscow_time = epoch

            else:
                Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

            title = f'@id{ban_users_info[0].id} (Пользователь) ' \
                    f'был заблокирован на {time_value} {time_type}.\n' \
                    f'Блокировка будет снята: {Moscow_time}\n' \
                    f'По снятию блокировки обращаться к @id{STUFF_ADMIN} (Администратору)'

            if time_value == '' and time_type == 'permanent':
                if DBtools.add_permanent_ban(message, ban_users_info[0].id):
                    await message.answer(title)
                    await ol.log_banned(message, ban_users_info, time_value, time_type)

                    await bot.api.messages.remove_chat_user(message.chat_id, message.reply_message.from_id)

            else:
                if DBtools.add_temp_ban(message, ban_users_info[0].id, time_value, time_type):
                    await message.answer(title)
                    await ol.log_banned(message, ban_users_info, time_value, time_type)

                    await bot.api.messages.remove_chat_user(message.chat_id, message.reply_message.from_id)

            message_id = message.reply_message.conversation_message_id
            peer_id = message.peer_id
            await bot.api.messages.delete(
                group_id=GROUP,
                peer_id=peer_id,
                cmids=message_id,
                delete_for_all=True
            )


@bl.chat_message(
    HandleCommand(ALIASES['ban_url'], ['!', '/'], 3),
    HandleLogConversation(False),
    PermissionAccess(1),
    PermissionIgnore(1),
    HandleRepliedMessages(False)
)
async def ban_url(message: Message, args: Tuple[str]):
    extractor = URLExtract()
    if extractor.has_urls(args[2]):
        shortname = ''

        if args[2].startswith('https://vk.com/id'):
            shortname = int(args[2].replace('https://vk.com/id', ''))

        elif args[2].startswith('https://vk.com/'):
            shortname = args[2].replace('https://vk.com/', '')

        print(shortname)
        if shortname != '':
            ban_users_info = await bot.api.users.get([shortname])

            print(ban_users_info)
            if ban_users_info:
                offset = datetime.timedelta(hours=3)
                tz = datetime.timezone(offset, name='МСК')

                time_value = args[0]
                time_type = TIME_TYPE[args[1]]

                if args[1] == 'p':
                    time_value = ''
                    epoch = '--'

                elif args[1] == 'm':
                    if int(time_value) < 0:
                        time_value = '1'
                    if int(time_value) > 12:
                        time_value = '12'
                    epoch = int(time.time()) + (31 * 24 * 60 * 60 * int(time_value))

                elif args[1] == 'd':
                    if int(time_value) < 0:
                        time_value = '1'
                    if int(time_value) > 31:
                        time_value = '31'
                    epoch = int(time.time()) + (24 * 60 * 60 * int(time_value))

                elif args[1] == 'h':
                    if int(time_value) < 0:
                        time_value = '1'
                    if int(time_value) > 24:
                        time_value = '24'
                    epoch = int(time.time()) + (60 * 60 * int(time_value))

                else:
                    time_value = '1'
                    time_type = TIME_TYPE['h']
                    epoch = int(time.time()) + (60 * 60 * 1)

                if epoch == '--':
                    Moscow_time = epoch

                else:
                    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

                title = f'@id{ban_users_info[0].id} (Пользователь) ' \
                        f'был заблокирован на {time_value} {time_type}.\n' \
                        f'Блокировка будет снята: {Moscow_time}\n' \
                        f'По снятию блокировки обращаться к @id{STUFF_ADMIN} (Администратору)'

                if time_value == '' and time_type == 'permanent':
                    if DBtools.add_permanent_ban(message, ban_users_info[0].id):
                        await message.answer(title)
                        await ol.log_banned_url(message, ban_users_info, time_value, time_type)

                        await bot.api.messages.remove_chat_user(message.chat_id, ban_users_info[0].id)

                else:
                    if DBtools.add_temp_ban(message, ban_users_info[0].id, time_value, time_type):
                        await message.answer(title)
                        await ol.log_banned_url(message, ban_users_info, time_value, time_type)

                        await bot.api.messages.remove_chat_user(message.chat_id, ban_users_info[0].id)


@bl.chat_message(
    HandleCommand(ALIASES['mute'], ['!', '/'], 2),
    HandleLogConversation(False),
    PermissionAccess(1),
    PermissionIgnore(1),
    HandleRepliedMessages(True)
)
async def mute(message: Message, args: Tuple[str]):
    if not message.fwd_messages:
        mute_users_info = await bot.api.users.get(message.reply_message.from_id)

        if mute_users_info:

            offset = datetime.timedelta(hours=3)
            tz = datetime.timezone(offset, name='МСК')

            time_value = args[0]
            time_type = TIME_TYPE[args[1]]

            if args[1] == 'm':
                if int(time_value) < 0:
                    time_value = '1'
                if int(time_value) > 12:
                    time_value = '12'
                epoch = int(time.time()) + (31 * 24 * 60 * 60 * int(time_value))

            elif args[1] == 'd':
                if int(time_value) < 0:
                    time_value = '1'
                if int(time_value) > 31:
                    time_value = '31'
                epoch = int(time.time()) + (24 * 60 * 60 * int(time_value))

            elif args[1] == 'h':
                if int(time_value) < 0:
                    time_value = '1'
                if int(time_value) > 24:
                    time_value = '24'
                epoch = int(time.time()) + (60 * 60 * int(time_value))

            else:
                time_value = '1'
                time_type = TIME_TYPE['h']
                epoch = int(time.time()) + (60 * 60 * 1)

            Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

            title = f'@id{mute_users_info[0].id} (Пользователь) ' \
                    f'был заглушен на {time_value} {time_type}.\n' \
                    f'Заглушение будет снято: {Moscow_time}\n' \
                    f'(При повторной попытке отправить сообщение, пользователь будет заблокирован)'

            if DBtools.add_mute(message, mute_users_info[0].id, time_value, time_type):
                await message.answer(title)
                await ol.log_muted(message, mute_users_info, time_value, time_type)

            message_id = message.reply_message.conversation_message_id
            peer_id = message.peer_id
            await bot.api.messages.delete(
                group_id=GROUP,
                peer_id=peer_id,
                cmids=message_id,
                delete_for_all=True
            )


@bl.chat_message(
    HandleCommand(ALIASES['mute_url'], ['!', '/'], 3),
    HandleLogConversation(False),
    PermissionAccess(1),
    PermissionIgnore(1),
    HandleRepliedMessages(False)
)
async def mute_url(message: Message, args: Tuple[str]):
    extractor = URLExtract()
    if extractor.has_urls(args[2]):
        shortname = ''
        if args[2].startswith('https://vk.com/id'):
            shortname = int(args[2].replace('https://vk.com/id', ''))

        elif args[2].startswith('https://vk.com/'):
            shortname = args[2].replace('https://vk.com/', '')

        if shortname != '':
            mute_users_info = await bot.api.users.get([shortname])

            if mute_users_info:
                offset = datetime.timedelta(hours=3)
                tz = datetime.timezone(offset, name='МСК')

                time_value = args[0]
                time_type = TIME_TYPE[args[1]]

                if args[1] == 'm':
                    if int(time_value) < 0:
                        time_value = '1'
                    if int(time_value) > 12:
                        time_value = '12'
                    epoch = int(time.time()) + (31 * 24 * 60 * 60 * int(time_value))

                elif args[1] == 'd':
                    if int(time_value) < 0:
                        time_value = '1'
                    if int(time_value) > 31:
                        time_value = '31'
                    epoch = int(time.time()) + (24 * 60 * 60 * int(time_value))

                elif args[1] == 'h':
                    if int(time_value) < 0:
                        time_value = '1'
                    if int(time_value) > 24:
                        time_value = '24'
                    epoch = int(time.time()) + (60 * 60 * int(time_value))

                else:
                    time_value = '1'
                    time_type = TIME_TYPE['h']
                    epoch = int(time.time()) + (60 * 60 * 1)

                Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

                title = f'@id{mute_users_info[0].id} (Пользователь) ' \
                        f'был заглушен на {time_value} {time_type}\n' \
                        f'Заглушение будет снято: {Moscow_time}\n' \
                        f'(При повторной попытке отправить сообщение, пользователь будет заблокирован)'

                if DBtools.add_mute(message, mute_users_info[0].id, time_value, time_type):
                    await message.answer(title)
                    await ol.log_muted_url(message, mute_users_info, time_value, time_type)


@bl.chat_message(
    HandleCommand(ALIASES['warn'], ['!', '/'], 0),
    HandleLogConversation(False),
    PermissionAccess(1),
    PermissionIgnore(1),
    HandleRepliedMessages(True)
)
async def warn(message: Message):
    if not message.fwd_messages:
        warn_users_info = await bot.api.users.get(message.reply_message.from_id)

        if warn_users_info:
            warn_count = DBtools.get_warn_count(message, warn_users_info[0].id)

            epoch = int(time.time()) + (24 * 60 * 60 * 1)

            offset = datetime.timedelta(hours=3)
            tz = datetime.timezone(offset, name='МСК')

            Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

            if DBtools.add_warn(message, warn_users_info[0].id, warn_count + 1):
                await ol.log_warned(message, warn_users_info, warn_count + 1)
                title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                        f'получил предупреждение [{warn_count + 1}/3].\n'
                if warn_count + 1 != 3:
                    title += f'Предупреждения будут сняты: {Moscow_time}'

                await message.answer(title)

            if warn_count + 1 == 3:
                reason = 'Получено 3 предупреждения'

                time_value = '1'
                time_type = TIME_TYPE['d']

                if DBtools.add_mute(message, warn_users_info[0].id, time_value, time_type):
                    title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                            f'был заглушен на {time_value} {time_type}.\n' \
                            f'Заглушение будет снято: {Moscow_time}\n' \
                            f'(При повторной попытке отправить сообщение, пользователь будет заблокирован)'
                    await message.answer(title)
                    await ol.log_system_muted(message, warn_users_info, time_value, time_type, reason)

            message_id = message.reply_message.conversation_message_id
            peer_id = message.peer_id
            await bot.api.messages.delete(
                group_id=GROUP,
                peer_id=peer_id,
                cmids=message_id,
                delete_for_all=True
            )


@bl.chat_message(
    HandleCommand(ALIASES['warn_url'], ['!', '/'], 1),
    HandleLogConversation(False),
    PermissionAccess(1),
    PermissionIgnore(1),
    HandleRepliedMessages(False)
)
async def warn_url(message: Message, args: Tuple[str]):
    extractor = URLExtract()
    if extractor.has_urls(args[0]):
        shortname = ''

        if args[0].startswith('https://vk.com/id'):
            shortname = int(args[0].replace('https://vk.com/id', ''))

        elif args[0].startswith('https://vk.com/'):
            shortname = args[0].replace('https://vk.com/', '')

        if shortname != '':
            warn_users_info = await bot.api.users.get([shortname])

            if warn_users_info:
                warn_count = DBtools.get_warn_count(message, warn_users_info[0].id)

                epoch = int(time.time()) + (24 * 60 * 60 * 1)

                offset = datetime.timedelta(hours=3)
                tz = datetime.timezone(offset, name='МСК')

                Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

                title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                        f'получил предупреждение [{warn_count + 1}/3].\n'
                if warn_count + 1 != 3:
                    title += f'Предупреждения будут сняты: {Moscow_time}'

                await message.answer(title)

                if DBtools.add_warn(message, warn_users_info[0].id, warn_count + 1):
                    await ol.log_warned_url(message, warn_users_info, warn_count + 1)

                if warn_count + 1 == 3:
                    reason = 'Получено 3 предупреждения'

                    time_value = '3'
                    time_type = TIME_TYPE['d']

                    if DBtools.add_mute(message, warn_users_info[0].id, time_value, time_type):
                        title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                                f'был заглушен на {time_value} {time_type}.\n' \
                                f'Заглушение будет снято: {Moscow_time}\n' \
                                f'(При повторной попытке отправить сообщение, пользователь будет заблокирован)'
                        await message.answer(title)
                        await ol.log_system_muted(message, warn_users_info, time_value, time_type, reason)


@bl.chat_message(
    HandleCommand(ALIASES['unban'], ['!', '/'], 0),
    HandleLogConversation(False),
    PermissionAccess(1),
    HandleRepliedMessages(True)
)
async def unban(message: Message):
    if not message.fwd_messages:
        unban_users_info = await bot.api.users.get(message.reply_message.from_id)

        if unban_users_info:
            user_id = unban_users_info[0].id

            ban_kind = DBtools.get_ban_kind(message, user_id)
            if ban_kind == 'permanent':
                if DBtools.remove_permanent_ban(message, user_id):
                    await ol.log_unbanned(message, unban_users_info)

            elif ban_kind == 'temp':
                if DBtools.remove_temp_ban(message, user_id):
                    await ol.log_unbanned(message, unban_users_info)


@bl.chat_message(
    HandleCommand(ALIASES['unban_url'], ['!', '/'], 1),
    HandleLogConversation(False),
    PermissionAccess(1),
    HandleRepliedMessages(False)
)
async def unban_url(message: Message, args: Tuple[str]):
    extractor = URLExtract()
    if extractor.has_urls(args[0]):
        shortname = ''

        if args[0].startswith('https://vk.com/id'):
            shortname = int(args[0].replace('https://vk.com/id', ''))

        elif args[0].startswith('https://vk.com/'):
            shortname = args[0].replace('https://vk.com/', '')

        if shortname != '':
            unban_users_info = await bot.api.users.get([shortname])

            if unban_users_info:
                user_id = unban_users_info[0].id

                ban_kind = DBtools.get_ban_kind(message, user_id)
                if ban_kind == 'permanent':
                    if DBtools.remove_permanent_ban(message, user_id):
                        await ol.log_unbanned_url(message, unban_users_info)

                elif ban_kind == 'temp':
                    if DBtools.remove_temp_ban(message, user_id):
                        await ol.log_unbanned_url(message, unban_users_info)


@bl.chat_message(
    HandleCommand(ALIASES['unmute'], ['!', '/'], 0),
    HandleLogConversation(False),
    PermissionAccess(1),
    HandleRepliedMessages(True)
)
async def unmute(message: Message):
    if not message.fwd_messages:

        unmute_users_info = await bot.api.users.get(message.reply_message.from_id)

        if unmute_users_info:
            user_id = unmute_users_info[0].id

            if DBtools.remove_mute(message, user_id):
                await ol.log_unmuted(message, unmute_users_info)


@bl.chat_message(
    HandleCommand(ALIASES['unmute_url'], ['!', '/'], 1),
    HandleLogConversation(False),
    PermissionAccess(1),
    HandleRepliedMessages(False)
)
async def unmute_url(message: Message, args: Tuple[str]):
    extractor = URLExtract()
    if extractor.has_urls(args[0]):
        shortname = ''

        if args[0].startswith('https://vk.com/id'):
            shortname = int(args[0].replace('https://vk.com/id', ''))

        elif args[0].startswith('https://vk.com/'):
            shortname = args[0].replace('https://vk.com/', '')

        if shortname != '':
            unmute_users_info = await bot.api.users.get([shortname])

            if unmute_users_info:
                user_id = unmute_users_info[0].id

                if DBtools.remove_mute(message, user_id):
                    await ol.log_unmuted_url(message, unmute_users_info)


@bl.chat_message(
    HandleCommand(ALIASES['unwarn'], ['!', '/'], 0),
    HandleLogConversation(False),
    PermissionAccess(1),
    HandleRepliedMessages(True)
)
async def unwarn(message: Message):
    if not message.fwd_messages:
        unwarn_users_info = await bot.api.users.get(message.reply_message.from_id)

        if unwarn_users_info:
            user_id = unwarn_users_info[0].id

            warn_count = DBtools.get_warn_count(message, user_id)

            if warn_count != 0:
                DBtools.remove_warn(message, user_id, warn_count)
                await ol.log_unwarned(message, unwarn_users_info, warn_count - 1)


@bl.chat_message(
    HandleCommand(ALIASES['unwarn_url'], ['!', '/'], 1),
    HandleLogConversation(False),
    PermissionAccess(1),
    HandleRepliedMessages(False)
)
async def unwarn_url(message: Message, args: Tuple[str]):
    extractor = URLExtract()

    if extractor.has_urls(args[0]):
        shortname = ''

        if args[0].startswith('https://vk.com/id'):
            shortname = int(args[0].replace('https://vk.com/id', ''))

        elif args[0].startswith('https://vk.com/'):
            shortname = args[0].replace('https://vk.com/', '')

        if shortname != '':
            unwarn_users_info = await bot.api.users.get([shortname])

            if unwarn_users_info:
                user_id = unwarn_users_info[0].id

                warn_count = DBtools.get_warn_count(message, user_id)

                if warn_count != 0:
                    DBtools.remove_warn(message, user_id, warn_count)
                    await ol.log_unwarned_url(message, unwarn_users_info, warn_count - 1)


@bl.chat_message(
    HandleCommand(ALIASES['delete'], ['!', '/'], 0),
    HandleLogConversation(True),
    PermissionAccess(1),
    HandleRepliedMessages(True)
)
async def delete(message: Message):
    if message.fwd_messages:
        await ol.log_deleted(message)

        for msg in message.fwd_messages:

            message_id = msg.conversation_message_id
            peer_id = message.peer_id
            await bot.api.messages.delete(
                group_id=GROUP,
                peer_id=peer_id,
                cmids=message_id,
                delete_for_all=True
            )

    else:
        await ol.log_deleted(message)

        message_id = message.reply_message.conversation_message_id
        peer_id = message.peer_id
        await bot.api.messages.delete(
            group_id=GROUP,
            peer_id=peer_id,
            cmids=message_id,
            delete_for_all=True
        )


@bl.chat_message(
    HandleCommand(ALIASES['set_permission'], ['!', '/'], 1),
    HandleLogConversation(True),
    PermissionAccess(2),
    HandleRepliedMessages(True)
)
async def set_permission(message: Message, args: Tuple[str]):
    if not message.fwd_messages:
        try:
            permission_lvl = int(args[0])  # Catching exception here

            if permission_lvl > 3 or permission_lvl < 0:
                permission_lvl = 0

            users_info = await bot.api.users.get(message.reply_message.from_id)

            if users_info:
                if DBtools.set_permission(message, users_info[0].id, permission_lvl):
                    await ol.log_permission_changed(message, users_info, permission_lvl)

        except TypeError:
            pass


@bl.chat_message(
    HandleCommand(ALIASES['set_permission_url'], ['!', '/'], 2),
    HandleLogConversation(True),
    PermissionAccess(2),
    HandleRepliedMessages(False)
)
async def set_permission_url(message: Message, args: Tuple[str]):
    try:
        permission_lvl = int(args[0])
        if permission_lvl > 3:
            permission_lvl = 0

        extractor = URLExtract()

        if extractor.has_urls(args[1]):
            shortname = ''

            if args[1].startswith('https://vk.com/id'):
                shortname = int(args[1].replace('https://vk.com/id', ''))

            elif args[1].startswith('https://vk.com/'):
                shortname = args[1].replace('https://vk.com/', '')

            if shortname != '':
                users_info = await bot.api.users.get([shortname])

                if DBtools.set_permission(message, users_info[0].id, permission_lvl):
                    await ol.log_permission_changed_url(message, users_info, permission_lvl)

    except TypeError:
        pass


@bl.chat_message(
    HandleCommand(ALIASES['set_cooldown'], ['!', '/'], 1),
    HandleLogConversation(False),
    PermissionAccess(2),
    HandleRepliedMessages(False)
)
async def set_cooldown(message: Message, args: Tuple[str]):
    try:
        cooldown = int(args[0])  # Catching exception here

        if DBtools.set_cooldown(message, cooldown):
            title = f'Задержка на сообщения для данной беседы установлена на {cooldown} second(s).'
            await message.answer(title)
            await ol.log_cooldown_changed(message, cooldown)

    except TypeError:
        pass


@bl.chat_message(
    HandleCommand(ALIASES['set_log_conversation'], ['!', '/'], 0),
    HandleLogConversation(True),
    PermissionAccess(2),
    HandleRepliedMessages(False)
)
async def set_log_conversation(message: Message):
    if DBtools.set_log_conversation(message):
        title = f'Данная беседа теперь назначена в качестве лог-чата.'
        await message.answer(title)
        await ol.log_log_conversation_changed(message)


@bl.chat_message(
    HandleCommand(ALIASES['change_setting'], ['!', '/'], 2),
    HandleLogConversation(False),
    PermissionAccess(2),
    HandleRepliedMessages(False)
)
async def change_setting(message: Message, args: Tuple[str]):
    try:
        setting = str(args[0])
        value = str(args[1]).lower()

        if value == 'true':
            value = True

        elif value == 'false':
            value = False

        if setting in SETTINGS and isinstance(value, bool):
            if DBtools.change_setting(message, setting, value):
                await ol.log_setting_changed(message, setting, value)

    except TypeError:
        pass


@bl.chat_message(
    HandleCommand(ALIASES['remove_from_queue'], ['!', '/'], 0),
    HandleLogConversation(False),
    PermissionAccess(1),
    HandleRepliedMessages(True)
)
async def remove_from_queue(message: Message):
    if not message.fwd_messages:
        users_info = await bot.api.users.get(message.reply_message.from_id)

        if users_info:
            if DBtools.remove_from_queue(message, users_info[0].id):
                await ol.log_removed_from_queue_url(message, users_info)


@bl.chat_message(
    HandleCommand(ALIASES['remove_from_queue_url'], ['!', '/'], 1),
    HandleLogConversation(False),
    PermissionAccess(1),
    HandleRepliedMessages(False)
)
async def remove_from_queue_url(message: Message, args: Tuple[str]):
    extractor = URLExtract()

    if extractor.has_urls(args[0]):
        shortname = ''

        if args[0].startswith('https://vk.com/id'):
            shortname = int(args[0].replace('https://vk.com/id', ''))

        elif args[0].startswith('https://vk.com/'):
            shortname = args[0].replace('https://vk.com/', '')

        if shortname != '':
            users_info = await bot.api.users.get([shortname])

            if DBtools.remove_from_queue(message, users_info[0].id):
                await ol.log_removed_from_queue_url(message, users_info)


@bl.chat_message(
    HandleCommand(ALIASES['get_permission'], ['!', '/'], 0),
    HandleLogConversation(True),
    HandleRepliedMessages(False)
)
async def get_permission(message: Message):
    if not DBtools.check_admins(message):
        members = await bot.api.messages.get_conversation_members(group_id=GROUP, peer_id=message.peer_id)
        members = members.items
        for member in members:
            if member.member_id == message.from_id and member.is_admin:
                users_info = await bot.api.users.get(message.from_id)
                permission_lvl = 2

                if users_info:
                    if DBtools.set_permission(message, users_info[0].id, permission_lvl):
                        title = f'Права администратора получены.\n Вы можете снять с себя VK Admin\n'
                        await message.answer(title)

                        await ol.log_system_permission_changed(message, users_info, permission_lvl)


@bl.chat_message(
    HandleCommand(ALIASES['msg_copy'], ['!', '/'], 0),
    PermissionAccess(2),
    HandleLogConversation(False),
    HandleRepliedMessages(True)
)
async def msg_copy(message: Message):
    if not message.fwd_messages:
        title = message.reply_message.text
        await message.answer(title)
        await ol.log_msg_copied(message)
