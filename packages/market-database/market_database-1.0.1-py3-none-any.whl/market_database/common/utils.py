import datetime
from importlib import resources
import logging
from pathlib import Path
import pickle
import sys
import typing as T
import json

from tinkoff.invest import CandleInterval

from market_database.common.types import Resource


INTERVALS = {
    "1m": CandleInterval.CANDLE_INTERVAL_1_MIN,
    "1h": CandleInterval.CANDLE_INTERVAL_HOUR,
    "1d": CandleInterval.CANDLE_INTERVAL_DAY,
}
MAX_CANDLES_TIMEDELTA = {
    "1m": datetime.timedelta(minutes=1),
    "1h": datetime.timedelta(hours=1),
    "1d": datetime.timedelta(days=1),
}
TICKER_FIGI_MAP_RESOURCE = Resource("market_database.configs", "ticker_figi_map.json")


def read_text_resource(resource: Resource) -> str:
    return resources.read_text(resource.package, resource.name)


def read_json(path: Path) -> T.Dict:
    with open(path, 'r') as input_file:
        return json.load(input_file)
    

def read_pickle(path: Path) -> T.Any:
    with open(path, "rb") as input_file:
        return pickle.load(input_file)
    

def dump_pickle(values: T.Any, path: Path):
    with open(path, "wb") as output_file:
        pickle.dump(values, output_file)


def get_ticker_figi_map() -> T.Dict[str, str]:
    return json.loads(read_text_resource(TICKER_FIGI_MAP_RESOURCE))

def is_valid_interval_name(interval_name: str) -> bool:
    return interval_name in INTERVALS


def is_valid_ticker(ticker: str) -> bool:
    return ticker in get_ticker_figi_map()


def get_interval_from_name(interval_name: str) -> CandleInterval:
    if interval_name not in INTERVALS:
        raise NotImplementedError(f"Interval with name {interval_name} is not implemented")
    
    return INTERVALS[interval_name]


def get_max_candles_delta(interval_name: str) -> datetime.timedelta:
    if interval_name not in INTERVALS:
        raise NotImplementedError(f"Interval with name {interval_name} is not implemented")
    
    return MAX_CANDLES_TIMEDELTA[interval_name]


def get_logger(name: str) -> logging.Logger:
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger
