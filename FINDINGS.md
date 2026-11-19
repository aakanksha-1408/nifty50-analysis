# NIFTY 50 Sector Analysis: Key Findings

Period: 2020-01-01 to 2026-11-18. Source: Yahoo Finance adjusted closing prices.

## Findings

1. **Banking grew [faster / slower] than IT:** Banking's average yearly growth (CAGR) was [BANK CAGR]%, compared with [IT CAGR]% for IT. Over this period, [Banking / IT] delivered the higher return. See `banking_vs_it.png`.

2. **[Banking / IT] carried more risk:** Annualised volatility was [BANK VOL]% for Banking and [IT VOL]% for IT, so [Banking / IT] prices swung more widely from day to day. See `volatility_banking_vs_it.png`.

3. **[Banking / IT] had the deeper worst fall:** The maximum drawdown was [BANK DD]% for Banking and [IT DD]% for IT, meaning [Banking / IT] lost more from its peak before recovering. See `sector_indices.png`.

4. **Banking stocks moved together [more / less] than IT stocks:** The average correlation of daily returns was [BANK CORR] for Banking and [IT CORR] for IT. Stocks that move together offer less protection when the sector falls. See `correlation_heatmap.png`.

## Method and caveats
- Sector indices are equal-weighted averages of daily returns, so large companies don't dominate.
- The stock list reflects NIFTY 50 constituents as of [CHECK DATE] (survivorship bias: companies that left the index are not included).
- Volatility is the standard deviation of daily returns, annualised by the square root of 252.
- Maximum drawdown is the largest peak-to-trough fall in the compounded return series.
- Data comes from Yahoo Finance, which is unofficial and may contain errors.
- Results depend on the period chosen and are not a forecast.