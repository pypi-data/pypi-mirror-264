from market_database.common import utils


def get_ticker_figi(ticker: str) -> str:
    figi_map = utils.get_ticker_figi_map()
    if ticker not in figi_map:
        raise NotImplementedError(f"FIGI mapping for ticker {ticker} is not implemented now")

    return figi_map[ticker]
