import datetime
import typing as T

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.schemas import HistoricCandle

from market_database.seeker import utils as seeker_utils


class HistoryDataSeeker:
    def __init__(self, api_token: str):
        self._api_token = api_token

    def seek(
        self,
        ticker: str,
        from_date: datetime.datetime,
        to_date: datetime.datetime,
        interval: CandleInterval
    ) -> T.List[HistoricCandle]:
        figi = seeker_utils.get_ticker_figi(ticker)

        with Client(self._api_token) as client:
            return list(client.get_all_candles(figi=figi, from_=from_date, to=to_date, interval=interval))
