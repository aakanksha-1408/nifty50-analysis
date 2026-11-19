"""Central configuration: stock universe, sectors, dates and parameters."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = BASE_DIR / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"

# Date range (YYYY-MM-DD). END_DATE = None means "up to today".
START_DATE = "2020-01-01"
END_DATE = None

# NIFTY 50 index, used as the market benchmark for beta.
BENCHMARK = "^NSEI"

# Analysis parameters
MA_WINDOWS = (20, 50, 200)   # moving-average windows in trading days
VOL_WINDOW = 21              # rolling volatility window (about one trading month)
TRADING_DAYS = 252           # used to annualise returns and volatility
RISK_FREE_RATE = 0.065       # approximate annual rate; update to the current T-bill yield
MAX_MISSING_FRACTION = 0.05  # drop a stock if more than 5% of its prices are missing
OUTLIER_RETURN = 0.25        # flag single-day moves larger than 25% for review

# NIFTY 50 constituents grouped by sector.
# Index membership changes over time. Verify this list against NSE's current NIFTY 50 list.
SECTORS = {
    "Banking": ["HDFCBANK", "ICICIBANK", "KOTAKBANK", "AXISBANK", "SBIN", "INDUSINDBK"],
    "Financial Services": ["BAJFINANCE", "BAJAJFINSV", "SHRIRAMFIN", "HDFCLIFE", "SBILIFE"],
    "IT": ["TCS", "INFY", "HCLTECH", "WIPRO", "TECHM"],
    "Energy & Power": ["RELIANCE", "ONGC", "BPCL", "COALINDIA", "NTPC", "POWERGRID"],
    "Auto": ["MARUTI", "M&M", "BAJAJ-AUTO", "EICHERMOT", "HEROMOTOCO"],
    "Pharma & Healthcare": ["SUNPHARMA", "DRREDDY", "CIPLA", "APOLLOHOSP"],
    "FMCG": ["HINDUNILVR", "ITC", "NESTLEIND", "BRITANNIA", "TATACONSUM"],
    "Metals": ["TATASTEEL", "JSWSTEEL", "HINDALCO"],
    "Industrials & Infra": ["LT", "ULTRACEMCO", "GRASIM", "ADANIENT", "ADANIPORTS", "BEL"],
    "Consumer Services": ["ASIANPAINT", "TITAN", "TRENT", "ETERNAL"],
    "Telecom": ["BHARTIARTL"],
}

NSE_SUFFIX = ".NS"
TICKER_SECTOR = {t: sector for sector, names in SECTORS.items() for t in names}
STOCK_TICKERS = list(TICKER_SECTOR)


def yahoo_symbol(ticker: str) -> str:
    """Convert a plain NSE symbol to Yahoo's format (TCS -> TCS.NS). Indices pass through."""
    return ticker if ticker.startswith("^") else f"{ticker}{NSE_SUFFIX}"
