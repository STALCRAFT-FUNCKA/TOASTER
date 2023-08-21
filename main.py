from vkbottle.bot import Bot
from config import TOKEN

from handlers import handlers
from routes import labelers

bot = Bot(token=TOKEN)


def _load(modules):
    for module in modules:
        bot.labeler.load(module)


@bot.loop_wrapper.interval(seconds=1)
async def check_punish_state():
    for handler in handlers:
        await handler.check()


if __name__ == "__main__":
    _load(labelers)

    bot.run_forever()
