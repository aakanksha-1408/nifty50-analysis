"""Clean raw price data: fix types, handle gaps, drop unusable series, flag outliers."""
import pandas as pd

from config import MAX_MISSING_FRACTION, OUTLIER_RETURN


def clean_prices(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df.index = pd.to_datetime(df.index)
    df = df[~df.index.duplicated(keep="last")].sort_index()
    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.where(df > 0)  # zero or negative prices are invalid

    # Drop series with too much missing data (delisted, or listed after START_DATE)
    missing = df.isna().mean()
    too_sparse = missing[missing > MAX_MISSING_FRACTION].index.tolist()
    if too_sparse:
        print(f"Dropping series with more than {MAX_MISSING_FRACTION:.0%} missing data: {too_sparse}")
    df = df.drop(columns=too_sparse)

    # Fill short gaps (up to 3 days), then drop rows that are still incomplete
    rows_before = len(df)
    df = df.ffill(limit=3).dropna(how="any")
    print(f"Removed {rows_before - len(df)} incomplete rows; {df.shape[1]} series remain.")
    return df


def flag_outliers(returns: pd.DataFrame) -> pd.Series:
    """Count suspiciously large daily moves per series. Review these by hand."""
    flags = (returns.abs() > OUTLIER_RETURN).sum()
    flags = flags[flags > 0]
    if not flags.empty:
        print(f"Daily moves larger than {OUTLIER_RETURN:.0%} (check for data errors or corporate actions):")
        print(flags.to_string())
    return flags
