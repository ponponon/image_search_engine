from datetime import datetime, timedelta, timezone
import time
import contextlib
from pydantic.datetime_parse import parse_datetime as pydantic_parse_datetime


def get_min_utc_timestamp() -> datetime:
    return (datetime(year=1970, month=1, day=1) + timedelta(seconds=1)).replace(tzinfo=timezone.utc)


def get_utc_now_timestamp(tzinfo: bool = True) -> datetime:
    """ https://blog.csdn.net/ball4022/article/details/101670024 """
    if tzinfo:
        return datetime.utcnow().replace(tzinfo=timezone.utc)
    else:
        return datetime.utcnow().replace(tzinfo=None)


def timedelta_seconds(start_time: datetime, end_time: datetime = None) -> int:
    """ 返回两个时间相差的秒数 """
    if not end_time:
        end_time = get_utc_now_timestamp()

    return int((end_time - start_time).total_seconds())


def custom_timestamp(base_timestamp: datetime, seconds: int, reduce=False):
    return base_timestamp + timedelta(seconds=seconds) \
        if not reduce \
        else base_timestamp - timedelta(seconds=seconds)


def parse_datetime(value: str) -> datetime | None:
    try:
        return pydantic_parse_datetime(value)
    except Exception:
        return None


def datetime2simplestring(d: datetime | None) -> str | None:
    return d.strftime('%Y-%m-%dT%H:%M:%S') if d else None


@contextlib.contextmanager
def timer(msg: str = None, logger=None):
    if not logger:
        from loguru import logger as loguru_logger
        logger = loguru_logger

    start = time.time()
    yield
    logger.debug(f'{msg}, used {round(time.time() - start,3)} s')
