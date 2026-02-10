from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {"open", "high", "low", "close"}


def load_csv(path: str) -> pd.DataFrame:
    """Load OHLCV CSV data.

    Expected columns: time, open, high, low, close (volume optional).
    """
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    try:
        df = pd.read_csv(csv_path)
    except Exception as exc:
        raise ValueError(f"Failed to read CSV '{csv_path}': {exc}") from exc

    if df.empty:
        raise ValueError(f"CSV '{csv_path}' is empty.")

    df.columns = [str(c).strip().lower() for c in df.columns]
    if "time" not in df.columns:
        raise ValueError("CSV must contain a 'time' column.")

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns: {sorted(missing)}")

    df["time"] = pd.to_datetime(df["time"], errors="coerce", utc=False)
    invalid_time = df["time"].isna().sum()
    if invalid_time:
        raise ValueError(f"Found {invalid_time} invalid datetime rows in 'time' column.")

    df = df.set_index("time").sort_index()

    for col in ["open", "high", "low", "close", "volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    bad_rows = df[["open", "high", "low", "close"]].isna().any(axis=1).sum()
    if bad_rows:
        raise ValueError(f"Found {bad_rows} rows with invalid OHLC numeric values.")

    return df
