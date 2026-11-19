# NIFTY 50 Stock Market Analysis

A Python project that analyses NIFTY 50 stocks using daily price data from Yahoo Finance. It calculates daily returns, moving averages, and volatility, and compares sectors such as Banking and IT. The results are shown in tables and charts.

## Tools used
Python, Pandas, yfinance, Matplotlib, Seaborn

## Project files
- `main.py`: runs the full analysis
- `data_loader.py`: downloads the price data
- `cleaning.py`: cleans the data
- `analysis.py`: calculates returns, moving averages, and volatility
- `visualize.py`: creates the charts
- `FINDINGS.md`: key findings and caveats

## How to run
```bash
pip install -r requirements.txt
python main.py --refresh
python -m pytest
```
