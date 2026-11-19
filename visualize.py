"""Charts saved to outputs/figures/."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config import FIGURE_DIR, TICKER_SECTOR

sns.set_theme(style="whitegrid", context="notebook")


def _save(fig, name: str) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURE_DIR / f"{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {path.name}")


def plot_lines(df, columns, title, ylabel, name, ref_line=None) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    for col in columns:
        ax.plot(df.index, df[col], label=col, linewidth=1.3)
    if ref_line is not None:
        ax.axhline(ref_line, color="grey", linestyle="--", linewidth=0.8)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.legend(ncol=2 if len(columns) > 4 else 1, fontsize=9)
    _save(fig, name)


def plot_price_with_mas(prices: pd.DataFrame, mas: dict, ticker: str) -> None:
    df = pd.DataFrame({"Close": prices[ticker]})
    for window, ma in mas.items():
        df[f"{window}-day MA"] = ma[ticker]
    plot_lines(df, list(df.columns), f"{ticker}: price and moving averages", "Price (INR)",
               f"price_ma_{ticker}")


def plot_correlation_heatmap(stock_returns: pd.DataFrame) -> None:
    order = sorted(stock_returns.columns, key=lambda t: TICKER_SECTOR.get(t, ""))
    corr = stock_returns[order].corr()
    fig, ax = plt.subplots(figsize=(14, 12))
    sns.heatmap(corr, cmap="RdBu_r", vmin=-1, vmax=1, center=0, square=True,
                cbar_kws={"shrink": 0.6}, ax=ax)
    ax.set_title("Daily return correlation (stocks grouped by sector)")
    _save(fig, "correlation_heatmap")


def plot_return_distribution(stock_returns: pd.DataFrame) -> None:
    long = stock_returns.stack().rename("daily_return").reset_index()
    long.columns = ["Date", "Ticker", "daily_return"]
    long["Sector"] = long["Ticker"].map(TICKER_SECTOR)
    order = long.groupby("Sector")["daily_return"].std().sort_values().index

    fig, ax = plt.subplots(figsize=(13, 6))
    sns.boxplot(data=long, x="Sector", y="daily_return", order=order,
                showfliers=False, ax=ax)
    ax.axhline(0, color="grey", linewidth=0.8)
    ax.tick_params(axis="x", rotation=30)
    ax.set_title("Distribution of daily returns by sector (least to most volatile)")
    ax.set_ylabel("Daily return")
    _save(fig, "return_distribution_by_sector")
