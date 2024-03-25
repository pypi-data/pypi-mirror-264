from typing import Dict, List
import datetime as dtm
import pandas as pd
import tempfile

from google.cloud.storage import Client


def get_tick_data(date: dtm.date, asset_code: str) -> pd.DataFrame:
    """
    해당 일 체결 정보를 반환합니다

    Args:
        date (dtm.date): 조회할 날짜
        asset_code (str): 조회할 종목 코드

    Returns:
        pd.DataFrame: 요청한 일자의 해당 종목의 모든 체결 정보를 담은 DataFrame

        - chetime (datetime.time): 체결시간
        - sign (str): 전일대비구분 (1:상한 2:상승 3:보함 4:하한 5:하락)
        - change (int): 전일대비가격
        - drate (float): 등락율
        - price (int): 체결가
        - opentime (datetime.time): 시가시간
        - open (int): 시가
        - hightime (datetime.time): 고가시간
        - high (int): 고가
        - lowtime (datetime.time): 저가시간
        - low (int): 저가
        - cgubun (str): 체결구분 (-:매도 +:매수 NaN:동시호가)
        - cvolume (int): 체결량
        - volume (int): 누적거래량
        - value (int): 누적거래대금
        - mdvolume (int): 매도체결수량
        - msvolume (int): 매수체결수량
        - mdchecnt (int): 매도체결건수
        - mschecnt (int): 매수체결건수
        - cpower (float): 체결강도
        - w_avrg (int): 가중평균가
        - offerho (int): 매도호가
        - bidho (int): 매수호가
        - status (str): 장정보 (0:장중 10:장전시간외 4:장후시간외 3:장마감)
        - jnilvolume (int): 전일거래량
        - shcode (str): 종목코드

    Examples:
        >>> df = get_tick_data(datetime.date.today() - datetime.timedelta(days=3), "017670")
        >>> print(df.head())
           mdchecnt  sign  mschecnt  mdvolume  w_avrg  cpower  offerho  cvolume   high  bidho    low  price cgubun  value  change  shcode  chetime  opentime  lowtime  volume  drate  hightime  jnilvolume  msvolume   open  status
        0         1     3         0        50   53200     0.0        0       50      0      0      0  53200      -      3       0   17670    83133       NaN      NaN      50    0.0       NaN           0         0      0      10
        1         2     3         0        54   53200     0.0        0        4      0      0      0  53200      -      3       0   17670    83316       NaN      NaN      54    0.0       NaN           0         0      0      10
        2         3     3         0        64   53200     0.0        0       10      0      0      0  53200      -      3       0   17670    83433       NaN      NaN      64    0.0       NaN           0         0      0      10
        3         3     3         0        64   53200     0.0    53300    12426  53200  53200  53200  53200    NaN    664       0   17670    90010   90010.0  90010.0   12490    0.0   90010.0           0         0  53200       0
        4         4     3         0       147   53200     0.0    53300       83  53200  53200  53200  53200      -    669       0   17670    90010   90010.0  90010.0   12573    0.0   90010.0           0         0  53200       0

    """

    storage_client = Client()
    bucket = storage_client.get_bucket("pyqqq-tick-data")
    blob = bucket.blob(f"{date}/{asset_code}.csv.xz")

    with tempfile.NamedTemporaryFile() as tmpfile:
        blob.download_to_filename(tmpfile.name)
        df = pd.read_csv(tmpfile.name, compression="xz")

        for k in ["opentime", "hightime", "lowtime", "chetime"]:
            df[k] = pd.to_datetime(df[k], format="%H%M%S").dt.time

    return df
