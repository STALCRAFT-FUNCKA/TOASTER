"""
Main project file.
"""

from vkbottle.bot import Bot
from config import TOKEN
from routes import handlers, labelers

bot = Bot(token=TOKEN)


def load(modules: list):
    """
    The function loads all BotLabelers one by one into the bot body.

    Args:
        modules (list): Any implemented list of BotLabelers from vkbottle.
    """
    for module in modules:
        bot.labeler.load(module)


@bot.loop_wrapper.interval(seconds=1)
async def check_punish_state():
    """
    A loop wrapper that provides a check for 
    changes in the state of punishments every second.
    """
    for handler in handlers:
        await handler.check()


if __name__ == "__main__":
    load(labelers)
    bot.run_forever()
