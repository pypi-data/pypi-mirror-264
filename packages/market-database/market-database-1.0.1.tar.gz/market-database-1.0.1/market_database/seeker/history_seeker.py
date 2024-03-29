import datetime
import logging
import time
import typing as T

import tinkoff.invest as ti

from market_database.common import utils
from market_database.seeker import utils as seeker_utils


logger = utils.get_logger(__name__)


class HistorySeeker:
    def __init__(self, api_token: str):
        self._api_token = api_token

    def seek(
        self,
        ticker: str,
        from_date: datetime.datetime,
        to_date: datetime.datetime,
        interval_name: str,
    ) -> T.Set[ti.schemas.HistoricCandle]:
        figi = seeker_utils.get_ticker_figi(ticker)
        interval = utils.get_interval_from_name(interval_name)

        candle_data = set()
        current_from_date = from_date
        with ti.Client(self._api_token) as client:
            while current_from_date < to_date:
                logger.info(f"Current request interval: {current_from_date} - {to_date}")
                try:
                    current_candles = list(client.get_all_candles(figi=figi, from_=current_from_date, to=to_date, interval=interval))
                    candle_data.update(current_candles)

                    next_from_date = max(candle.time for candle in current_candles).replace(tzinfo=None)
                    if next_from_date == current_from_date:
                        break
                    current_from_date = next_from_date
                except ti.exceptions.RequestError as e:
                    sleep_time = e.metadata.ratelimit_reset
                    logger.info(f"Wait {sleep_time} seconds")
                    time.sleep(sleep_time)

        return candle_data
