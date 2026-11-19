# NIFTY 50 Stock Market Analysis

Python analysis of NIFTY 50 stocks: daily returns, moving averages, volatility, and a Banking vs IT sector comparison, with Matplotlib and Seaborn charts.

## Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Get the data

Either download from Yahoo Finance (needs internet):

```bash
python main.py --refresh
```

or use your own CSV files: put one per ticker in `my_data/` (with `Date` and `Close` columns), then run `python build_dataset.py` and `python main.py`.

## Run

```bash
python main.py       # uses cached data if present
python -m pytest     # run the tests
```

## Outputs

- `outputs/sector_summary.csv`, `outputs/stock_summary.csv`: performance tables
- `outputs/rolling_volatility.csv`: 21-day annualised volatility per stock
- `outputs/figures/`: charts
- `FINDINGS.md`: write-up template to fill in with your results

## Configuration

Edit `config.py` to change the date range, sector membership, moving-average windows, or the risk-free rate.
