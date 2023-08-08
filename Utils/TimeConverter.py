import datetime


class Converter:
    @staticmethod
    def convert(epoch) -> str:
        offset = datetime.timedelta(hours=3)
        tz = datetime.timezone(offset, name='MSK')

        MSK_time = str(datetime.datetime.fromtimestamp(epoch, tz=tz)).split('+')[0]
        if MSK_time.find('.') != -1:
            MSK_time = MSK_time[0:MSK_time.find('.')]
        return MSK_time
