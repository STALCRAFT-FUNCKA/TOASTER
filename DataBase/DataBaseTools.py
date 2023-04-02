import json
import time
from json import JSONDecodeError

from vkbottle.bot import Message

from Log import Logger as ol


def create_pattern():
    with open("DataBase/DB.json", "w") as write_file:
        pattern = {
            'LogConversationID': 0,
            'Conversations': []
        }

        json.dump(pattern, write_file, indent=4)


def check_db():
    try:
        with open("DataBase/DB.json", "r") as read_file:
            try:
                json.load(read_file)
                print('DEBUG: DB is ready')

            except JSONDecodeError:
                print('WARNING: Data Base file is empty')
                print('DEBUG: Making DB pattern')
                create_pattern()
                print('DEBUG: New DB is ready')

    except FileNotFoundError:
        print('WARNING: Data Base file not found')
        print('DEBUG: Creating DB file and making pattern')
        create_pattern()
        print('DEBUG: New DB is ready')


def add_conversation(message: Message):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            return True

    conversation_pattern = {
        'PeerID': message.peer_id,
        'Permissions': {
            'Moderators': [],
            'Administrators': []
        },
        'Settings': {
            'Allow_Picture': True,
            'Allow_Video': True,
            'Allow_Music': True,
            'Allow_Voice': True,
            'Allow_Post': True,
            'Allow_Votes': True,
            'Allow_Files': True,
            'Allow_Miniapp': True,
            'Allow_Graffiti': True,
            'Allow_Sticker': True,
            'Allow_Reply': True,
            'Allow_AgeCheck': False,
            'Allow_URLCheck': True
        },
        'PermanentBannedUsers': [],
        'TempBannedUsers': [],
        'MutedUsers': [],
        'WarnedUsers': [],
        'MessageCooldownQueue': {
            'Cooldown': 0,
            'Queue': []
        }
    }

    database['Conversations'].append(conversation_pattern)

    with open("DataBase/DB.json", "w") as write_file:
        json.dump(database, write_file, indent=4)

    return False


def add_permanent_ban(message: Message, user_id):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:

            for user in conversation['PermanentBannedUsers']:
                if user['UserID'] == user_id:
                    return False

            permanent_ban_pattern = {
                'UserID': user_id,
                'UserURL': f'https://vk.com/id{user_id}',
                'BannedByID': message.from_id,
                'BannedByURL': f'https://vk.com/id{message.from_id}'
            }

            conversation['PermanentBannedUsers'].append(permanent_ban_pattern)

            with open("DataBase/DB.json", "w") as write_file:
                json.dump(database, write_file, indent=4)

            return True


def remove_permanent_ban(message: Message, user_id):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            place = 0
            for user in conversation['PermanentBannedUsers']:
                if user['UserID'] == user_id:
                    conversation['PermanentBannedUsers'].pop(place)

                    with open("DataBase/DB.json", "w") as write_file:
                        json.dump(database, write_file, indent=4)

                    return True

                place += 1

    return False


def add_temp_ban(message: Message, user_id, current_time, time_type):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    epoch_time = int(time.time())

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            for user in conversation['TempBannedUsers']:
                if user['UserID'] == user_id:
                    return False
            modify = 1

            if time_type == 'month(s)':
                modify = 31 * 24 * 60 * 60
            if time_type == 'day(s)':
                modify = 24 * 60 * 60
            if time_type == 'hour(s)':
                modify = 60 * 60

            summary_time = int(current_time) * modify

            temp_ban_pattern = {
                'UserID': user_id,
                'UserURL': f'https://vk.com/id{user_id}',
                'BanTime': epoch_time,
                'BanClearTime': epoch_time + summary_time
            }

            conversation['TempBannedUsers'].append(temp_ban_pattern)

            with open("DataBase/DB.json", "w") as write_file:
                json.dump(database, write_file, indent=4)

            return True

    return False


def remove_temp_ban(message: Message, user_id):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            place = 0
            for user in conversation['TempBannedUsers']:
                if user['UserID'] == user_id:
                    conversation['TempBannedUsers'].pop(place)

                    with open("DataBase/DB.json", "w") as write_file:
                        json.dump(database, write_file, indent=4)

                    return True

            place += 1

    return False


def get_ban_kind(message: Message, user_id):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            for user in conversation['TempBannedUsers']:
                if user['UserID'] == user_id:
                    return 'temp'

            for user in conversation['PermanentBannedUsers']:
                if user['UserID'] == user_id:
                    return 'permanent'

    return None


def add_mute(message: Message, user_id, current_time, time_type):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    epoch_time = int(time.time())

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            for user in conversation['MutedUsers']:
                if user['UserID'] == user_id:
                    return False
            modify = 1

            if time_type == 'month(s)':
                modify = 31 * 24 * 60 * 60
            if time_type == 'day(s)':
                modify = 24 * 60 * 60
            if time_type == 'hour(s)':
                modify = 60 * 60

            summary_time = int(current_time) * modify

            mute_pattern = {
                'UserID': user_id,
                'UserURL': f'https://vk.com/id{user_id}',
                'MuteTime': epoch_time,
                'MuteClearTime': epoch_time + summary_time
            }

            conversation['MutedUsers'].append(mute_pattern)

            with open("DataBase/DB.json", "w") as write_file:
                json.dump(database, write_file, indent=4)

            return True

    return False


def remove_mute(message: Message, user_id):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            place = 0
            for user in conversation['MutedUsers']:
                if user['UserID'] == user_id:
                    conversation['MutedUsers'].pop(place)

                    with open("DataBase/DB.json", "w") as write_file:
                        json.dump(database, write_file, indent=4)

                    return True

            place += 1

    return False


def check_mute(message: Message, user_id):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            for user in conversation['MutedUsers']:
                if user['UserID'] == user_id:
                    return True

            return False

    return False


def add_warn(message: Message, user_id, warn_count):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    epoch_time = int(time.time())

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            if warn_count == 3:
                place = 0
                for user in conversation['WarnedUsers']:
                    if user['UserID'] == user_id:
                        conversation['WarnedUsers'].pop(place)

                        with open("DataBase/DB.json", "w") as write_file:
                            json.dump(database, write_file, indent=4)

                        return True

                    place += 1

            elif warn_count == 2:
                for user in conversation['WarnedUsers']:
                    if user['UserID'] == user_id:
                        user['WarnCount'] = warn_count
                        user['LastWarnTime'] = epoch_time
                        user['WarnClearTime'] = epoch_time + (24 * 60 * 60)

                        with open("DataBase/DB.json", "w") as write_file:
                            json.dump(database, write_file, indent=4)

                        return True

            else:
                warn_pattern = {
                    'UserID': user_id,
                    'UserURL': f'https://vk.com/id{user_id}',
                    'WarnCount': warn_count,
                    'LastWarnTime': epoch_time,
                    'WarnClearTime': epoch_time + (24 * 60 * 60)
                }

                conversation['WarnedUsers'].append(warn_pattern)

                with open("DataBase/DB.json", "w") as write_file:
                    json.dump(database, write_file, indent=4)

                return True

    return False


def remove_warn(message: Message, user_id, warn_count):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            for user in conversation['WarnedUsers']:
                place = 0
                if user['UserID'] == user_id:
                    if warn_count - 1 == 0:
                        conversation['WarnedUsers'].pop(place)

                        with open("DataBase/DB.json", "w") as write_file:
                            json.dump(database, write_file, indent=4)

                        return True

                    else:
                        user['WarnCount'] = warn_count - 1

                        with open("DataBase/DB.json", "w") as write_file:
                            json.dump(database, write_file, indent=4)

                        return True

                place += 1

    return False


def get_warn_count(message: Message, user_id):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            for user in conversation['WarnedUsers']:
                if user['UserID'] == user_id:
                    return user['WarnCount']

    return 0


def check_permission(message: Message, user_id, permission_lvl):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    if permission_lvl == 0:
        return True

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:

            lvl = 1
            for user in conversation['Permissions']['Moderators']:
                if user['UserID'] == user_id and permission_lvl <= lvl:
                    return True

            lvl = 2
            for user in conversation['Permissions']['Administrators']:
                if user['UserID'] == user_id and permission_lvl <= lvl:
                    return True

    return False


def set_permission(message: Message, user_id, permission_lvl):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:

            added = False
            removed = False

            lvl = 1
            found = False
            for user in conversation['Permissions']['Moderators']:
                if user['UserID'] == user_id:
                    found = True
            if not found and lvl == permission_lvl:
                permission_pattern = {
                    'UserID': user_id,
                    'UserURL': f'https://vk.com/id{user_id}',
                    'PermissionLvl': 1
                }
                conversation['Permissions']['Moderators'].append(permission_pattern)
                added = True
            elif found and lvl != permission_lvl:
                permission_pattern = {
                    'UserID': user_id,
                    'UserURL': f'https://vk.com/id{user_id}',
                    'PermissionLvl': 1
                }
                conversation['Permissions']['Moderators'].remove(permission_pattern)
                removed = True

            lvl = 2
            found = False
            for user in conversation['Permissions']['Administrators']:
                if user['UserID'] == user_id:
                    found = True
            if not found and lvl == permission_lvl:
                permission_pattern = {
                    'UserID': user_id,
                    'UserURL': f'https://vk.com/id{user_id}',
                    'PermissionLvl': 2
                }
                conversation['Permissions']['Administrators'].append(permission_pattern)
                added = True
            elif found and lvl != permission_lvl:
                permission_pattern = {
                    'UserID': user_id,
                    'UserURL': f'https://vk.com/id{user_id}',
                    'PermissionLvl': 2
                }
                conversation['Permissions']['Administrators'].remove(permission_pattern)
                removed = True

            if added or removed:
                with open("DataBase/DB.json", "w") as write_file:
                    json.dump(database, write_file, indent=4)

                return True
            else:
                return False

    return False


def get_permission(message: Message, user_id):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:

            for user in conversation['Permissions']['Moderators']:
                if user['UserID'] == user_id:
                    return user['PermissionLvl'] or 1

            for user in conversation['Permissions']['Administrators']:
                if user['UserID'] == user_id:
                    return user['PermissionLvl'] or 2

    return 0


def set_cooldown(message: Message, cooldown):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            conversation['MessageCooldownQueue']['Cooldown'] = cooldown

            with open("DataBase/DB.json", "w") as write_file:
                json.dump(database, write_file, indent=4)

            return True

    return False


def get_cooldown(message: Message):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            return conversation['MessageCooldownQueue']['Cooldown']

    return 0


def set_log_conversation(message: Message):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    if database['LogConversationID'] == message.peer_id:
        return False

    else:
        database['LogConversationID'] = message.peer_id

        with open("DataBase/DB.json", "w") as write_file:
            json.dump(database, write_file, indent=4)

        return True


def get_log_conversation():
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    return database['LogConversationID']


def check_message_queue(message: Message):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    epoch_time = int(time.time())

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            for user in conversation['MessageCooldownQueue']['Queue']:
                if user['UserID'] == message.from_id:
                    if user['NextDispatchTime'] <= epoch_time:
                        return True

                    else:
                        return False

            return True

    return False


def add_to_message_queue(message: Message):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    epoch_time = int(time.time())

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            for user in conversation['MessageCooldownQueue']['Queue']:
                if user['UserID'] == message.from_id:
                    user['DispatchTime'] = epoch_time
                    user['NextDispatchTime'] = epoch_time + conversation['MessageCooldownQueue']['Cooldown']

                    with open("DataBase/DB.json", "w") as write_file:
                        json.dump(database, write_file, indent=4)

                    return True

            queue_pattern = {
                'UserID': message.from_id,
                'DispatchTime': epoch_time,
                'NextDispatchTime': epoch_time + conversation['MessageCooldownQueue']['Cooldown']
            }

            conversation['MessageCooldownQueue']['Queue'].append(queue_pattern)

            with open("DataBase/DB.json", "w") as write_file:
                json.dump(database, write_file, indent=4)

            return True

    return False


def get_setting(message: Message, setting: str):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            if setting in conversation['Settings']:
                return conversation['Settings'][setting]

            else:
                return False

    return False


def change_setting(message: Message, setting: str, value: bool):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            conversation['Settings'][setting] = value

            with open("DataBase/DB.json", "w") as write_file:
                json.dump(database, write_file, indent=4)

            return True

    return False


async def check_provisional_punish():
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    epoch_time = int(time.time())

    for conversation in database['Conversations']:
        if conversation['TempBannedUsers']:
            place = 0
            for user in conversation['TempBannedUsers']:
                if user['BanClearTime'] <= epoch_time:
                    conversation['TempBannedUsers'].pop(place)
                    await ol.log_system_temp_ban_removed(conversation['PeerID'], user['UserID'])
                place += 1

        if conversation['MutedUsers']:
            place = 0
            for user in conversation['MutedUsers']:
                if user['MuteClearTime'] <= epoch_time:
                    conversation['MutedUsers'].pop(place)
                    await ol.log_system_mute_removed(conversation['PeerID'], user['UserID'])
                place += 1

        if conversation['WarnedUsers']:
            place = 0
            for user in conversation['WarnedUsers']:
                if user['WarnClearTime'] <= epoch_time:
                    conversation['WarnedUsers'].pop(place)
                    await ol.log_system_warn_removed(conversation['PeerID'], user['UserID'])
                place += 1

        if conversation['MessageCooldownQueue']['Queue']:
            place = 0
            for user in conversation['MessageCooldownQueue']['Queue']:
                if user['NextDispatchTime'] <= epoch_time:
                    conversation['MessageCooldownQueue']['Queue'].pop(place)
                place += 1

    with open("DataBase/DB.json", "w") as write_file:
        json.dump(database, write_file, indent=4)


def get_punished_users():
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    conversations = {}

    for conversation in database['Conversations']:
        users = []

        if conversation['PermanentBannedUsers']:
            for user in conversation['PermanentBannedUsers']:
                users.append(user['UserID'])

        if conversation['TempBannedUsers']:
            for user in conversation['TempBannedUsers']:
                users.append(user['UserID'])

        conversations[conversation['PeerID']] = users

    return conversations


def remove_from_queue(message: Message, user_id: int):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            place = 0
            for user in conversation['MessageCooldownQueue']['Queue']:
                if user['UserID'] == user_id:
                    conversation['MessageCooldownQueue']['Queue'].pop(place)

                    with open("DataBase/DB.json", "w") as write_file:
                        json.dump(database, write_file, indent=4)

                    return True

                place += 1

    return False


def check_admins(message: Message):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            if not conversation['Permissions']['Administrators']:
                return False

            return True

    return True