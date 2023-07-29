from vkbottle.bot import Bot, BotLabeler, Message
from DataBase.Utils import Connection
from Config import ALIASES, TOKEN
from Rules.CustomRules import (HandleCommand)


bot = Bot(token=TOKEN)
database = Connection('database.db')
bl = BotLabeler()


"""
Команда вывода справки\справочной информации.
"""
@bl.chat_message(
    HandleCommand(ALIASES['reference'], ['!', '/'], 0)
)
async def reference(message: Message):
    url = 'https://github.com/Oidaho/FUNCKA-BOT/blob/master/README.md'

    title = f'Перейдя по этой ссылке, вы сможете найти документацию на GitHub:\n {url}'
    await message.answer(title)


"""
Команда регистрации беседы. 
Бот не будет производить никаких действий в беседе, пока она не будет зарегистрирована.
"""
@bl.chat_message(
    HandleCommand(ALIASES['somecommand'], ['!', '/'], 0)
)
async def enroll(message: Message):
    pass


"""
Команда регистрации лог-чата. 
Таких лог-чатов может быть несколько.
Бот отправляет логи своих действий в каждый из помеченных этой командой чатов.
"""
@bl.chat_message(
    HandleCommand(ALIASES['somecommand'], ['!', '/'], 0)
)
async def assign_log(message: Message):
    pass

@bl.chat_message(
    HandleCommand(ALIASES['somecommand'], ['!', '/'], 0)
)
async def unassign_log(message: Message):
    pass


"""
Команда кика пользователя с беседы. 
Бессрочно исключает пользователя из беседы.
"""
@bl.chat_message(
    HandleCommand(ALIASES['somecommand'], ['!', '/'], 0)
)
async def kick(message: Message):
    pass


"""
Команда бана пользователя в беседе. 
Временно исключает пользователя из беседы.
"""
@bl.chat_message(
    HandleCommand(ALIASES['somecommand'], ['!', '/'], 0)
)
async def ban(message: Message):
    pass

@bl.chat_message(
    HandleCommand(ALIASES['somecommand'], ['!', '/'], 0)
)
async def unban(message: Message):
    pass


"""
Команда заглушения пользователя в беседе. 
Временно не позволяет пользователю писать сообщения.
"""
@bl.chat_message(
    HandleCommand(ALIASES['somecommand'], ['!', '/'], 0)
)
async def mute(message: Message):
    pass

@bl.chat_message(
    HandleCommand(ALIASES['somecommand'], ['!', '/'], 0)
)
async def unmute(message: Message):
    pass


"""
Команда заглушения пользователя в беседе. 
Временно не позволяет пользователю писать сообщения.
"""
@bl.chat_message(
    HandleCommand(ALIASES['somecommand'], ['!', '/'], 0)
)
async def warn(message: Message):
    pass

@bl.chat_message(
    HandleCommand(ALIASES['somecommand'], ['!', '/'], 0)
)
async def unwarn(message: Message):
    pass