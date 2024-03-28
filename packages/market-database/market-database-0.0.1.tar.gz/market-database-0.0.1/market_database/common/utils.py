from pathlib import Path
import pickle
import typing as T
import json

from tinkoff.invest import CandleInterval


INTERVALS = {
    "1m": CandleInterval.CANDLE_INTERVAL_1_MIN,
    "1h": CandleInterval.CANDLE_INTERVAL_HOUR,
    "1d": CandleInterval.CANDLE_INTERVAL_DAY,
}
TICKER_FIGI_MAP_PATH = Path("market_database/configs/ticker_figi_map.json")


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
    return read_json(TICKER_FIGI_MAP_PATH)


def is_valid_interval_name(interval_name: str) -> bool:
    return interval_name in INTERVALS


def is_valid_ticker(ticker: str) -> bool:
    return ticker in get_ticker_figi_map()


def get_interval_from_name(interval_name: str) -> CandleInterval:
    if interval_name not in INTERVALS:
        raise NotImplementedError(f"Interval with name {interval_name} is not implemented")
    
    return INTERVALS[interval_name]
