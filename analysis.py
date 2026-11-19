"""Returns, moving averages, volatility, sector indices and performance metrics."""
import numpy as np
import pandas as pd

from config import MA_WINDOWS, RISK_FREE_RATE, TICKER_SECTOR, TRADING_DAYS, VOL_WINDOW


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna(how="any")


def moving_averages(prices: pd.DataFrame, windows=MA_WINDOWS) -> dict:
    return {w: prices.rolling(window=w).mean() for w in windows}


def rolling_volatility(returns: pd.DataFrame, window: int = VOL_WINDOW) -> pd.DataFrame:
    """Annualised rolling standard deviation of daily returns."""
    return returns.rolling(window=window).std() * np.sqrt(TRADING_DAYS)


def sector_returns(stock_returns: pd.DataFrame, sector_map: dict = TICKER_SECTOR) -> pd.DataFrame:
    """Equal-weighted average daily return for each sector (rows = dates, columns = sectors)."""
    mapper = pd.Series(sector_map)
    return stock_returns.T.groupby(mapper).mean().T


def max_drawdown(returns: pd.Series) -> float:
    """Largest peak-to-trough fall of the compounded return series."""
    index = (1 + returns).cumprod()
    return (index / index.cummax() - 1).min()


def performance_table(returns: pd.DataFrame, bench_returns: pd.Series | None = None) -> pd.DataFrame:
    """Annualised performance metrics for each column of daily returns."""
    years = (returns.index[-1] - returns.index[0]).days / 365.25
    total = (1 + returns).prod() - 1
    cagr = (1 + total) ** (1 / years) - 1
    vol = returns.std() * np.sqrt(TRADING_DAYS)
    sharpe = (returns.mean() * TRADING_DAYS - RISK_FREE_RATE) / vol

    table = pd.DataFrame({
        "total_return": total,
        "cagr": cagr,
        "ann_volatility": vol,
        "sharpe": sharpe,
        "max_drawdown": returns.apply(max_drawdown),
    })
    if bench_returns is not None:
        table["beta"] = returns.apply(lambda s: s.cov(bench_returns) / bench_returns.var())
    return table


def average_pairwise_correlation(corr: pd.DataFrame, tickers: list) -> float:
    """Average correlation between every pair of tickers in the list."""
    n = len(tickers)
    if n < 2:
        return float("nan")
    sub = corr.loc[tickers, tickers].to_numpy()
    return (sub.sum() - n) / (n * (n - 1))  # remove the diagonal of 1s
