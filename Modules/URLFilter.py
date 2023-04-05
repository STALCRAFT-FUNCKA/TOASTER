import datetime
import time

from vkbottle.bot import Bot, BotLabeler, Message
from Log import Logger as ol
from urlextract import URLExtract
from DataBase import DataBaseTools as DBtools
from Config import GROUP, TOKEN
from Rules.CustomRules import PermissionSelfIgnore, HandleLogConversation

bot = Bot(token=TOKEN)
bl = BotLabeler()

exceptions = [
    'https://forum.exbo.net',  # Форум
    'https://vk.com/funcka',  # Фанка
    'https://vk.cc/ca5l9d',  # Таблица расщепления
    'https://stalcalc.ru',  # Сталкалк от Вируса
    'https://vk.cc/c9RYhW', 'https://disk.yandex.ru/d/2LNeePtemDTsNg',  # Музыка с радио
    'https://vk.com/write-2677092',  # Техническая поддержка в ВК
    'https://stalcraft.net',  # Сайт сталкрафта
    'https://exbo.net',  # Сайт EXBO
    'https://support.exbo.net',  # Техническая поддержка на сайте EXBO
    'https://t.me/stalcraft',  # Канал сталкрафта в телеграмме
    'https://discord.com/invite/stalcraft',   # Дискорд сталкрафта
    'https://store.steampowered.com/app/1818450/STALCRAFT',  # Ссылка на сталкрафт в стиме
    'https://www.twitch.tv/exbo_official',  # Твитч канал EXBO
    'https://www.youtube.com/c/EXBO_official',  # Ютуб канал EXBO
    'https://www.tiktok.com/@stalcraft_official',   # Тикток сталкрафта
    'https://www.facebook.com/stalcraft.official',  # Фейсбук сталкрафта
    'https://twitter.com/STALCRAFT_ENG',  # Твиттер сталкрафта
    'https://www.instagram.com/stalcraft_official',  # Инстаграм сталкрафта
    'https://www.instagram.com/exbo_studio'  # Инстаграм EXBO
 ]


@bl.chat_message(
    HandleLogConversation(False),
    PermissionSelfIgnore(1),
    blocking=False
)
async def check_URL(message: Message):
    if DBtools.get_setting(message, 'Allow_URLCheck'):

        if message.deleted is None:

            extractor = URLExtract()

            if extractor.has_urls(message.text):
                found = False

                for url in exceptions:
                    if message.text.startswith(url):
                        found = True

                if not found:
                    mute_users_info = await bot.api.users.get(message.from_id)

                    message_id = message.conversation_message_id
                    await bot.api.messages.delete(
                        group_id=GROUP,
                        peer_id=message.peer_id,
                        cmids=message_id,
                        delete_for_all=True
                    )
                    message.deleted = True

                    time_value = '1'
                    time_type = 'hour(s)'

                    reason = 'Внешние ссылки'

                    epoch = int(time.time()) + (24 * 60 * 60 * 1)

                    offset = datetime.timedelta(hours=3)
                    tz = datetime.timezone(offset, name='МСК')

                    Moscow_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]

                    await ol.log_system_muted(message, mute_users_info, time_value, time_type, reason)

                    title = f'Подозрительная активность @id{mute_users_info[0].id} (участника) (Внешние ссылки)\n'\
                            f'@id{mute_users_info[0].id} (Пользователь) ' \
                            f'был заглушен на {time_value} {time_type} в целях безопасности\n' \
                            f'Заглушение будет снято: {Moscow_time}\n' \
                            f'(При повторной попытке отправить сообщение, пользователь будет заблокирован)'

                    await message.answer(title)

                    DBtools.add_mute(message, message.from_id, time_value, time_type)
