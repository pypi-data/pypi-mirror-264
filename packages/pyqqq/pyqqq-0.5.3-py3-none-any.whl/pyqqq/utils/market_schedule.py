"""
주식 거래소의 개장/폐장 시간을 확인하는 함수를 제공합니다.
"""

import datetime as dtm
from dataclasses import dataclass
from typing import Optional


@dataclass
class MarketSchedule:
    full_day_closed: bool
    exchange: str = 'KRX'
    open_time: Optional[dtm.time] = None
    close_time: Optional[dtm.time] = None
    reason: Optional[str] = None


def is_full_day_closed(exchange: str = "KRX") -> bool:
    """
    주식 거래소가 휴장일인지 확인합니다.

    Args:
        exchange (str): 거래소 이름

    Returns:
        bool: 휴장일 여부
    """

    assert exchange in ["KRX"], "지원하지 않는 거래소 코드입니다."

    # TODO: 국가별 (임시) 공휴일 처리
    return dtm.datetime.now().weekday() in [5, 6]


def is_before_opening(exchange: str = "KRX"):
    """
    주식 거래소가 아직 개장 전인지 확인합니다.

    Args:
        exchange (str): 거래소 이름

    Returns:
        bool: 개장 전 여부
    """
    assert exchange in ["KRX"], "지원하지 않는 거래소 코드입니다."

    now = dtm.datetime.now()

    # TODO: 국가별 (임시) 개장 시간 처리
    return now.time() < dtm.time(9, 0, 0)


def is_after_closing(exchange: str = "KRX"):
    """
    주식 거래소가 이미 폐장 후인지 확인합니다.

    Args:
        exchange (str): 거래소 이름

    Returns:
        bool: 폐장 후 여부
    """
    assert exchange in ["KRX"], "지원하지 않는 거래소 코드입니다."

    now = dtm.datetime.now()

    # TODO: 국가별 (임시) 폐장 시간 처리
    return now.time() > dtm.time(15, 30, 0)


def is_trading_time(exchange: str = "KRX"):
    """
    주식 거래소가 거래 시간인지 확인합니다.

    Args:
        exchange (str): 거래소 이름

    Returns:
        bool: 거래 시간 여부
    """
    assert exchange in ["KRX"], "지원하지 않는 거래소 코드입니다."

    return not (is_full_day_closed() or is_before_opening() or is_after_closing())


def get_market_schedule(date: dtm.date, exchange: str = "KRX") -> MarketSchedule:
    """
    주식 거래소의 개장/폐장 시간을 확인합니다.

    Args:
        date (datetime.date): 날짜
        exchange (str): 거래소 이름

    Returns:
        MarketSchedule: 거래소 개장/폐장 정보
    """

    full_day_closed = date.weekday() in [5, 6]

    if not full_day_closed:
        open_time = dtm.time(9, 0, 0)
        close_time = dtm.time(15, 30, 0)
        reason = None
    else:
        open_time = None
        close_time = None
        reason = '주말'

    return MarketSchedule(exchange=exchange,
                          full_day_closed=full_day_closed,
                          open_time=open_time,
                          close_time=close_time,
                          reason=reason)


def get_last_trading_day(date: dtm.date = None) -> dtm.date:
    """
    주어진 날짜의 직전 거래일을 반환합니다.

    Args:
        date (datetime.date): 날짜. 기본값: 오늘

    Returns:
        datetime.date: 직전 거래일
    """
    if date is None:
        date = dtm.date.today()

    while True:
        date -= dtm.timedelta(days=1)
        schedule = get_market_schedule(date)
        if schedule.full_day_closed:
            continue
        else:
            return date
