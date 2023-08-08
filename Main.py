from vkbottle.bot import Bot
from Config import TOKEN

from Handlers import handlers
from Labelers import labelers

bot = Bot(token=TOKEN)


def _load(modules):
    for module in modules:
        bot.labeler.load(module)


@bot.loop_wrapper.interval(seconds=1)
async def check_punish_state():
    for handler in handlers:
        handler.check()


if __name__ == "__main__":
    _load(labelers)

    bot.run_forever()
