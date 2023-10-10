"""
This file contains the converter class.
"""

import datetime
import time
from singltone import MetaSingleton
from config import TIME_COEFFICIENT


class Converter(metaclass=MetaSingleton):
    """
    A converter class whose main functions perform
    time processing in the local context.
    """

    @staticmethod
    def convert(epoch: int):
        """
        Converts time in seconds that have passed since epoch into a date and time 
        convenient for human representation in Moscow.

        Args:
            epoch (int): seconds since epoch.

        Returns:
            str: formated date string.
        """
        offset = datetime.timedelta(hours=3)
        tz = datetime.timezone(offset, name='MSK')

        msk_time = str(datetime.datetime.fromtimestamp(
            epoch,
            tz=tz
        )).split('+', maxsplit=-1)[0]
        if msk_time.find('.') != -1:
            msk_time = msk_time[0:msk_time.find('.')]
        return msk_time

    @staticmethod
    def now():
        """
        Returns now time in seconds.

        Returns:
            int: time in seconds.
        """
        return int(time.time())

    @staticmethod
    def delta(t: int, coefficient: str):
        """
        Returns a time delta equal to the number of specified hours/days/months.

        Args:
            t (int): time "count".
            coefficient (str): time type coefficient (h - hour; d - day; m - month) 

        Returns:
            int: time delta in seconds.
        """
        coefficient = TIME_COEFFICIENT[coefficient]
        if t > 0:
            return t * coefficient

        return coefficient
