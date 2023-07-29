from vkbottle.bot import Bot
from Config import TOKEN
from Labelers import labelers

bot = Bot(token=TOKEN)

if __name__ == "__main__":
    @bot.loop_wrapper.interval(seconds=1)
    async def check_punish_state():
        Ellipsis # TODO: Сделать проверку наказаний каждую секунду


    for custom_labeler in labelers:
        bot.labeler.load(custom_labeler)

    bot.run_forever()
