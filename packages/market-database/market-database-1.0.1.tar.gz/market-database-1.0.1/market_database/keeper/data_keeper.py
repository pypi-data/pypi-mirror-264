import datetime
from pathlib import Path
import typing as T

from market_database.common import utils

from tinkoff.invest import HistoricCandle


class DataKeeper:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def _check_ticker_dir(self, ticker_dir: Path):
        for interval_dir in ticker_dir.iterdir():
            if not utils.is_valid_interval_name(interval_dir.name):
                raise RuntimeError(f"{interval_dir.name} is not a valid interval name with path {interval_dir}")

    def _check_database(self):
        for ticker_dir in self.db_path.iterdir():
            if not ticker_dir.is_dir():
                raise RuntimeError(f"Path {ticker_dir} is not a directory")
            if not utils.is_valid_ticker(ticker_dir.name):
                raise RuntimeError(f"{ticker_dir.name} is not a valid ticker with path {ticker_dir}")

    def _check_ticker(self, ticker: str):
        if not utils.is_valid_ticker(ticker):
            raise ValueError(f"{ticker} is not a valid ticker")

    def _check_interval_name(self, interval: str):
        if not utils.is_valid_interval_name(interval):
            raise ValueError(f"{interval} is not a valid interval name")

    def create_database(self):
        self.db_path.mkdir()

    def init(self):
        if not self.db_path.exists():
            self.create_database()
        self._check_database()

    def _get_ticker_data_path(self, ticker: str, interval: str) -> Path:
        return self.db_path / ticker / interval

    def _read_ticker_data(self, ticker: str, interval: str) -> T.Set[HistoricCandle]:
        return utils.read_pickle(self._get_ticker_data_path(ticker, interval))

    def _write_ticker_data(self, data: T.Set[HistoricCandle], ticker: str, interval: str):
        ticker_data_path = self._get_ticker_data_path(ticker, interval)
        utils.dump_pickle(data, ticker_data_path)

    def get_ticker_data(
        self, ticker: str, from_date: datetime.datetime, to_date: datetime.datetime, interval: str
    ) -> T.Set[HistoricCandle]:
        self._check_ticker(ticker)
        self._check_interval_name(interval)

        ticker_data = self._read_ticker_data(ticker, interval)
        return [candle for candle in ticker_data if candle.time >= from_date and candle.time < to_date]

    def set_ticker_data(self, data: T.Set[HistoricCandle], ticker: str, interval: str):
        self._check_ticker(ticker)
        self._check_interval_name(interval)

        ticker_data = self._read_ticker_data(ticker, interval)
        ticker_data.update(data)
