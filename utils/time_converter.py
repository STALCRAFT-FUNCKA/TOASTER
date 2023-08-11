import datetime

from config import TIME_COEFFICENT


class Converter:
    @staticmethod
    def convert(epoch) -> str:
        offset = datetime.timedelta(hours=3)
        tz = datetime.timezone(offset, name='MSK')

        MSK_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]
        if MSK_time.find('.') != -1:
            MSK_time = MSK_time[0:MSK_time.find('.')]
        return MSK_time

    @staticmethod
    def delta(time, coefficent):
        try:
            time = int(time)
            coefficent = TIME_COEFFICENT[coefficent]

            if time > 0:
                return time * coefficent
            else:
                return coefficent

        except Exception as error:
            print("Converting aborted. Returning standard delta: ", error)
            return TIME_COEFFICENT["h"]
