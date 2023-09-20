import datetime
import time
from singltone import MetaSingleton
from src_config import TIME_COEFFICIENT


class Converter(metaclass=MetaSingleton):

    @staticmethod
    def convert(epoch) -> str:
        offset = datetime.timedelta(hours=3)
        tz = datetime.timezone(offset, name='MSK')

        MSK_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]
        if MSK_time.find('.') != -1:
            MSK_time = MSK_time[0:MSK_time.find('.')]
        return MSK_time

    @staticmethod
    def now():
        return int(time.time())

    @staticmethod
    def delta(t, coefficient):
        try:
            t = int(t)
            coefficient = TIME_COEFFICIENT[coefficient]

            if t > 0:
                return t * coefficient
            else:
                return coefficient

        except Exception as error:
            print("Converting aborted. Returning standard delta: ", error)
            return TIME_COEFFICIENT["h"]
