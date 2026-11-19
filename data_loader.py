"""Download daily adjusted close prices from Yahoo Finance via yfinance."""
import time

import pandas as pd
import yfinance as yf

from config import BENCHMARK, END_DATE, RAW_DIR, START_DATE, STOCK_TICKERS, yahoo_symbol

CACHE_FILE = RAW_DIR / "close_prices.csv"


def download_prices(use_cache: bool = True, retries: int = 3) -> pd.DataFrame:
    """Return a DataFrame of closing prices (rows = dates, columns = tickers)."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if use_cache and CACHE_FILE.exists():
        print(f"Using cached data: {CACHE_FILE}")
        return pd.read_csv(CACHE_FILE, index_col=0, parse_dates=True)

    symbols = [yahoo_symbol(t) for t in STOCK_TICKERS] + [BENCHMARK]

    for attempt in range(1, retries + 1):
        try:
            raw = yf.download(
                symbols,
                start=START_DATE,
                end=END_DATE,
                auto_adjust=True,   # adjusts for splits and dividends
                progress=False,
            )
            close = raw["Close"]
            if close.dropna(how="all").empty:
                raise ValueError("Yahoo Finance returned no data")
            break
        except Exception as exc:
            print(f"Download attempt {attempt} failed: {exc}")
            if attempt == retries:
                raise
            time.sleep(5 * attempt)

    close.columns = [c.replace(".NS", "") for c in close.columns]
    close.index.name = "Date"
    close.to_csv(CACHE_FILE)
    print(f"Downloaded and cached {close.shape[1]} series to {CACHE_FILE}")
    return close
