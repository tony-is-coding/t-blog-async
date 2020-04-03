# coding:utf8
"""
    时间转换工具类
"""
import calendar
import time
from datetime import datetime, timedelta, timezone

utc_offset = time.timezone
SECOND_PER_DAY = 60 * 60 * 24
INIT_DAYS = 719528  # 公元0年到1970-01-01 的天数


def get_now_mil_timestamp() -> int:
    """:return current time ms timestamp - 13 bit"""
    return int(time.time() * 1000)


def get_utc_now() -> datetime:
    """ :return current utc datetime """
    return datetime.now(timezone.utc)


def get_utc_by_period(utc_time: datetime, period: str) -> datetime:
    """
    :param utc_time: utc datetime
    :param period: -1M/-1H/-1d/-1m, +1M/+1H/+1d/+1m
    :return:
    """
    period_v, period_type = int(period[:-1]), period[-1:]
    if period_type == "d":
        return utc_time + timedelta(days=period_v)
    else:
        return utc_time


def ms_timestamp_to_utc(timestamp: int) -> datetime:
    """ ms timestamp to datetime
    :type timestamp:int
    :rtype: datetime
    """
    return datetime.utcfromtimestamp(timestamp / 1000.0)


def timestamp_to_utc(timestamp: int) -> datetime:
    """ second timestamp to datetime

    :type timestamp:int
    :rtype: datetime
    """
    return datetime.utcfromtimestamp(timestamp)


def datetime_to_timestamp(v: datetime):
    """
    datetime: no tzinfo / local server datetime  datetime 转10位时间戳
    """
    v = time.mktime(v.timetuple())
    return v - utc_offset


def datetime_to_ms_timestamp(v: datetime):
    """日期转毫秒时间戳 -- 13 位"""
    return int(calendar.timegm(v.timetuple()) * 1000.0 + v.microsecond / 1000.0)


def str_to_timestamp(string: str):
    """日期时间字符串转时间戳 - 13位"""
    import time
    return int(time.mktime(time.strptime(string, "%Y-%m-%d")) * 1000)


def ms_str_to_timestamp(string: str):
    """秒级时间字符串转时间戳 - 10 位"""
    return time.mktime(time.strptime(string, "%Y-%m-%d %H:%M:%S"))


def date_format(dt: datetime):
    return f"{dt.year}-{dt.month}-{dt.day}"


def date_time_format(dt: datetime):
    return dt.strftime('%Y-%m-%d  %H:%M:%S')


def ms_ts_to_dt(ts):
    """毫秒时间戳转日期"""
    return date_format(timestamp_to_utc(int(ts / 1000)))


def s_ts_to_dt(ts):
    """秒级时间戳转日期"""
    return date_format(timestamp_to_utc(int(ts)))


def ms_ts_to_dtt(ts):
    """毫秒时间戳转日期时间"""
    return date_time_format(timestamp_to_utc(int(ts / 1000)))


def s_ts_to_dtt(ts):
    """秒级时间戳转日期时间"""
    return date_time_format(timestamp_to_utc(int(ts)))

