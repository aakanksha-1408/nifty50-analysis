"""Run the full NIFTY 50 analysis pipeline.

Usage:
    python main.py            # use cached data if it exists
    python main.py --refresh  # re-download from Yahoo Finance
"""
import argparse

import pandas as pd

from analysis import (
    average_pairwise_correlation,
    daily_returns,
    moving_averages,
    performance_table,
    rolling_volatility,
    sector_returns,
)
from cleaning import clean_prices, flag_outliers
from config import BENCHMARK, OUTPUT_DIR, PROCESSED_DIR, TICKER_SECTOR
from data_loader import download_prices
from visualize import (
    plot_correlation_heatmap,
    plot_lines,
    plot_price_with_mas,
    plot_return_distribution,
)

HIGHLIGHT_STOCKS = ["HDFCBANK", "TCS"]  # shown in detail with moving averages


def print_key_numbers(stock_stats: pd.DataFrame, sector_stats: pd.DataFrame,
                      stock_returns: pd.DataFrame) -> None:
    """Print the numbers you need to back up your findings."""
    stocks = stock_stats.drop(index=BENCHMARK)
    cols = ["cagr", "ann_volatility", "sharpe", "max_drawdown", "beta"]

    print("\n=== SECTOR PERFORMANCE (equal-weighted, sorted by CAGR) ===")
    print(sector_stats.sort_values("cagr", ascending=False).round(3).to_string())

    print("\n=== TOP 5 STOCKS BY CAGR ===")
    print(stocks.nlargest(5, "cagr")[cols].round(3).to_string())

    print("\n=== BOTTOM 5 STOCKS BY CAGR ===")
    print(stocks.nsmallest(5, "cagr")[cols].round(3).to_string())

    print("\n=== MOST VOLATILE 5 ===")
    print(stocks.nlargest(5, "ann_volatility")[cols].round(3).to_string())

    print("\n=== LEAST VOLATILE 5 ===")
    print(stocks.nsmallest(5, "ann_volatility")[cols].round(3).to_string())

    corr = stock_returns.corr()
    print("\n=== AVERAGE PAIRWISE CORRELATION OF DAILY RETURNS ===")
    for name in ["Banking", "IT"]:
        tickers = [t for t in stocks.index if TICKER_SECTOR.get(t) == name]
        print(f"  {name:<12} {average_pairwise_correlation(corr, tickers):.2f}")
    print(f"  {'All stocks':<12} {average_pairwise_correlation(corr, list(stocks.index)):.2f}")


def run(refresh: bool = False) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load and clean
    raw = download_prices(use_cache=not refresh)
    prices = clean_prices(raw)
    prices.to_csv(PROCESSED_DIR / "clean_prices.csv")

    # 2. Returns
    returns = daily_returns(prices)
    flag_outliers(returns)
    bench = returns[BENCHMARK]
    stock_returns = returns.drop(columns=[BENCHMARK])
    stock_prices = prices.drop(columns=[BENCHMARK])

    # 3. Moving averages and volatility per stock
    mas = moving_averages(stock_prices)
    vol = rolling_volatility(stock_returns)

    # 4. Sector analysis
    sector_ret = sector_returns(stock_returns)
    sector_idx = (1 + sector_ret).cumprod() * 100
    sector_vol = rolling_volatility(sector_ret)

    # 5. Performance tables
    stock_stats = performance_table(returns, bench_returns=bench)
    stock_stats["sector"] = [TICKER_SECTOR.get(t, "Benchmark") for t in stock_stats.index]
    sector_stats = performance_table(sector_ret)
    stock_stats.to_csv(OUTPUT_DIR / "stock_summary.csv")
    sector_stats.to_csv(OUTPUT_DIR / "sector_summary.csv")
    vol.to_csv(OUTPUT_DIR / "rolling_volatility.csv")

    # 6. Charts
    for ticker in HIGHLIGHT_STOCKS:
        if ticker in stock_prices.columns:
            plot_price_with_mas(stock_prices, mas, ticker)
        else:
            print(f"Skipping {ticker} chart: not in the cleaned data.")
    plot_lines(sector_idx, list(sector_idx.columns),
               "Equal-weighted sector indices (start = 100)", "Index level",
               "sector_indices", ref_line=100)
    plot_lines(sector_idx, ["Banking", "IT"],
               "Banking vs IT: cumulative performance", "Index level",
               "banking_vs_it", ref_line=100)
    plot_lines(sector_vol, ["Banking", "IT"],
               "Banking vs IT: 21-day rolling volatility (annualised)", "Volatility",
               "volatility_banking_vs_it")
    plot_correlation_heatmap(stock_returns)
    plot_return_distribution(stock_returns)

    # 7. Numbers for the write-up
    print_key_numbers(stock_stats, sector_stats, stock_returns)
    print(f"\nDone. Tables are in {OUTPUT_DIR}, charts in {OUTPUT_DIR / 'figures'}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NIFTY 50 stock market analysis")
    parser.add_argument("--refresh", action="store_true",
                        help="re-download data instead of using the cache")
    args = parser.parse_args()
    run(refresh=args.refresh)
