"""_summary_
"""
import time
from datetime import (
    timedelta,
    timezone,
    datetime
)


def timestamp() -> int:
    """Returns the count of seconds that
    have passed since epoch.

    Returns:
        int: Seconds since epoch.
    """
    ts = int(time.time())

    return ts


def time_zone() -> timezone:
    """Returns the Object of the datetime 
    time zone Moscow (UTC +3).

    Returns:
        timezone: Moscow time zone object.
    """
    offset = timedelta(hours=3)
    tz = timezone(offset, name='MSK')

    return tz


def msk_now() -> str:
    """Returns the line with the
    current Moscow datetime.

    Returns:
        str: _description_
    """
    msk_time = str(datetime.fromtimestamp(
        timestamp(),
        tz=time_zone()
    )).split('+', maxsplit=-1)[0]

    if msk_time.find('.') != -1:
        msk_time = msk_time[0:msk_time.find('.')]

    return msk_time


def msk_delta(hours: int = 0, minutes: int = 0, seconds: int =0) -> str:
    """Returns the line with the
    delta Moscow datetime.

    Args:
        hours (int, optional): Hours delta. Defaults to 0.
        minutes (int, optional): Minutes delta. Defaults to 0.
        seconds (int, optional): Seconds delta. Defaults to 0.

    Returns:
        str: _description_
    """
    delta = timedelta(
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )

    msk_time = datetime.fromtimestamp(
        timestamp(),
        tz=time_zone()
    )
    msk_time += delta
    msk_time = str(msk_time).split('+', maxsplit=-1)[0]

    if msk_time.find('.') != -1:
        msk_time = msk_time[0:msk_time.find('.')]

    return msk_time


if __name__ == "__main__":
    print(msk_now)
