import datetime

import requests
from Log import Logger as ol
from bs4 import BeautifulSoup
from vkbottle.bot import Bot, BotLabeler, Message
from Config import TOKEN, GROUP, STUFF_ADMIN

bot = Bot(token=TOKEN)
bl = BotLabeler()


@bl.chat_message(
    blocking=False
)
async def check_age(message: Message):

    response = requests.get(f'https://vk.com/foaf.php?id={message.from_id}')
    user_xml = response.text

    soup = BeautifulSoup(user_xml, "xml")

    if 'banned' not in soup.Person.profileState:
        created_at = str(soup.Person.created)
        created_at = created_at[created_at.find('\"') + 1:]
        created_at = created_at[:created_at.find('\"')].replace('T', ' ')
        created_at = created_at[:created_at.find('+')]

        aca = datetime.datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
        n = datetime.datetime.now()

        delta = n - aca
        delta_seconds = int(delta.total_seconds())

        week = 60 * 60 * 24 * 7

        if delta_seconds < week:

            reason = 'Аккаунт моложе недели'

            mute_users_info = await bot.api.users.get(message.from_id)

            time_value = ''
            time_type = 'permanent'

            title = f'@id{mute_users_info[0].id} (Пользователь) ' \
                    f'был заблокирован на {time_value} {time_type}\n' \
                    f'Причина: {reason}\n' \
                    f'Блокировка будет снята: --\n' \
                    f'По снятию блокировки общаться к @id{STUFF_ADMIN} (Администратору)'

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
