import datetime
import time

from vkbottle.bot import Bot, BotLabeler, Message

from Config import TOKEN, GROUP, STUFF_ADMIN
from DataBase import DataBaseTools as DBtools
from Log import Logger as ol
from Rules.CustomRules import PermissionSelfIgnore, HandleLogConversation

bot = Bot(token=TOKEN)
bl = BotLabeler()


@bl.chat_message(
    PermissionSelfIgnore(1),
    HandleLogConversation(False),
    blocking=False
)
async def check_message_queue(message: Message):
    if message.deleted is None:

        if DBtools.check_mute(message, message.from_id):
            DBtools.remove_mute(message, message.from_id)

            reason = 'Нарушено заглушение'

            mute_users_info = await bot.api.users.get(message.from_id)

            time_value = '3'
            time_type = 'day(s)'

            epoch = int(time.time()) + (3 * 24 * 60 * 60 * 1)

            offset = datetime.timedelta(hours=3)
            tz = datetime.timezone(offset, name='МСК')

            Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

            if DBtools.add_temp_ban(message, message.from_id, time_value, time_type):
                title = f'@id{mute_users_info[0].id} (Пользователь) ' \
                        f'был заблокирован на {time_value} {time_type}\n' \
                        f'Блокировка будет снята: {Moscow_time}\n' \
                        f'По снятию блокировки обращаться к @id{STUFF_ADMIN} (Администратору)'
                await message.answer(title)
                await ol.log_system_banned(message, mute_users_info, time_value, time_type, reason)

                message_id = message.conversation_message_id
                await bot.api.messages.delete(
                    group_id=GROUP,
                    peer_id=message.peer_id,
                    cmids=message_id,
                    delete_for_all=True
                )
                message.deleted = True

                await bot.api.messages.remove_chat_user(message.chat_id, message.from_id)

        elif DBtools.get_cooldown(message) != 0:
            if DBtools.check_message_queue(message):
                DBtools.add_to_message_queue(message)

            else:
                warn_users_info = await bot.api.users.get(message.from_id)
                warn_count = DBtools.get_warn_count(message, message.from_id)

                epoch = int(time.time()) + (24 * 60 * 60 * 1)

                offset = datetime.timedelta(hours=3)
                tz = datetime.timezone(offset, name='МСК')

                Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

                reason = 'Нарушение задержки'

                title = f'Остынь! Соблюдай медленный режим.\n' \
                        f'@id{message.from_id} (Пользователь) получил предупреждение [{warn_count + 1}/3]\n'
                if warn_count + 1 != 3:
                    title += f'Предупреждения будут сняты: {Moscow_time}'

                await message.answer(title)
                await ol.log_system_warned(message, warn_users_info, warn_count + 1, reason)

                message_id = message.conversation_message_id
                await bot.api.messages.delete(
                    group_id=GROUP,
                    peer_id=message.peer_id,
                    cmids=message_id,
                    delete_for_all=True
                )
                message.deleted = True

                DBtools.add_warn(message, message.from_id, warn_count + 1)

                if warn_count + 1 == 3:
                    reason = 'Получено 3 предупреждения'
                    mute_users_info = await bot.api.users.get(message.from_id)

                    time_value = '1'
                    time_type = 'day(s)'

                    if DBtools.add_mute(message, message.from_id, time_value, time_type):
                        title = f'@id{mute_users_info[0].id} (Пользователь) ' \
                                f'был заглушен на {time_value} {time_type}\n' \
                                f'Заглушение будет снято: {Moscow_time}\n' \
                                f'(При повторной попытке отправить сообщение, пользователь будет заблокирован)'

                        await message.answer(title)
                        await ol.log_system_muted(message, mute_users_info, time_value, time_type, reason)
