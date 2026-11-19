import numpy as np
import pandas as pd

from analysis import max_drawdown, sector_returns
from cleaning import clean_prices


def test_clean_replaces_zero_price_and_leaves_no_gaps():
    # 100 rows so one bad price (1%) stays under the 5% missing-data limit
    idx = pd.bdate_range("2023-01-02", periods=100)
    prices = np.full(100, 10.0)
    prices[50] = 0.0
    out = clean_prices(pd.DataFrame({"X": prices}, index=idx))
    assert out.shape == (100, 1)
    assert out.isna().sum().sum() == 0
    assert out.iloc[50, 0] == 10.0  # zero replaced by forward fill


def test_max_drawdown_matches_hand_calculation():
    # 1.10 -> 0.55 -> 0.66: the worst fall is 50% from the peak
    r = pd.Series([0.10, -0.50, 0.20])
    assert np.isclose(max_drawdown(r), -0.5)


def test_sector_returns_are_equal_weighted():
    idx = pd.bdate_range("2023-01-02", periods=3)
    r = pd.DataFrame({"HDFCBANK": [0.01, 0.02, 0.03],
                      "ICICIBANK": [0.03, 0.04, 0.05]}, index=idx)
    s = sector_returns(r)
    assert np.allclose(s["Banking"], [0.02, 0.03, 0.04])
