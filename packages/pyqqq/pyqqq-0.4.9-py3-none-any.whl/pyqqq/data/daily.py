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
    """

    storage_client = Client()
    bucket = storage_client.get_bucket("pyqqq-tick-data")
    blob = bucket.blob(f"{date}/{asset_code}.csv.xz")

    with tempfile.NamedTemporaryFile() as tmpfile:
        blob.download_to_filename(tmpfile.name)
        df = pd.read_csv(tmpfile.name, compression="xz")

    return df
