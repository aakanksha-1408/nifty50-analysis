"""Build data/raw/close_prices.csv from your own downloaded CSV files.

Put one CSV per ticker in a folder called my_data/ (for example TCS.csv or ^NSEI.csv).
Each file needs a Date column and a Close column. Then run: python build_dataset.py
"""
from pathlib import Path

import pandas as pd

from config import RAW_DIR

SOURCE_DIR = Path("my_data")

frames = {}
for f in sorted(SOURCE_DIR.glob("*.csv")):
    df = pd.read_csv(f, parse_dates=["Date"], index_col="Date")
    if "Close" not in df.columns:
        raise ValueError(f"{f.name} has no 'Close' column; rename the column or edit this script")
    frames[f.stem] = df["Close"]

if not frames:
    raise SystemExit(f"No CSV files found in {SOURCE_DIR}/")

close = pd.DataFrame(frames).sort_index()
close.index.name = "Date"

RAW_DIR.mkdir(parents=True, exist_ok=True)
close.to_csv(RAW_DIR / "close_prices.csv")
print(f"Wrote {close.shape[0]} rows x {close.shape[1]} series to {RAW_DIR / 'close_prices.csv'}")
