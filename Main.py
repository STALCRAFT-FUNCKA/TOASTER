from DataBase import DataBaseTools as DBtools
from vkbottle.bot import Bot
from Config import TOKEN
from Modules import labelers


if __name__ == "__main__":
    DBtools.check_db()

    bot = Bot(token=TOKEN)


    @bot.loop_wrapper.interval(seconds=1)
    async def check_provisional_punish():
        await DBtools.check_provisional_punish()


    for custom_labeler in labelers:
        bot.labeler.load(custom_labeler)

    bot.run_forever()
