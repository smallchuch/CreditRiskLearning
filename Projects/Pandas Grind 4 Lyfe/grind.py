"""
Pandas Grind 4 Lyfe - data loader.

    from grind import load
    loan = load('loan')                      # a fresh DataFrame every call
    snap = load('loan_monthly_snapshot')

The Parquet files come from the Synthetic Bank database (the same data as SQL Grind 4 Lyfe).
Two conversions happen on load, so you work with normal pandas types:
  * money / rate / ratio columns (stored as exact decimals) -> float64
  * date columns -> datetime64 (so .dt works)

Tables are cached in memory after the first load, and every call returns a copy,
so changing a DataFrame in one answer can never leak into another.
"""
import json
import os

import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ROOT, "config.json")) as _f:
    _CFG = json.load(_f)
PARQUET_DIR = _CFG["parquet_dir"]
if not os.path.isabs(PARQUET_DIR):
    PARQUET_DIR = os.path.normpath(os.path.join(ROOT, PARQUET_DIR))

_CACHE = {}


def _read(name):
    path = os.path.join(PARQUET_DIR, name + ".parquet")
    if not os.path.exists(path):
        raise FileNotFoundError(f"no table called '{name}' (looked for {path}). Available: {', '.join(tables())}")
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
        t = pq.read_table(path)
        fields = []
        for f in t.schema:
            if pa.types.is_decimal(f.type):
                fields.append(pa.field(f.name, pa.float64()))
            elif pa.types.is_date(f.type):
                fields.append(pa.field(f.name, pa.timestamp("ns")))
            else:
                fields.append(f)
        return t.cast(pa.schema(fields)).to_pandas()
    except ImportError:
        import datetime
        import decimal
        df = pd.read_parquet(path)
        for c in df.columns:
            if df[c].dtype == object:
                first = df[c].dropna()
                first = first.iloc[0] if len(first) else None
                if isinstance(first, decimal.Decimal):
                    df[c] = df[c].astype(float)
                elif isinstance(first, datetime.date):
                    df[c] = pd.to_datetime(df[c])
        return df


def load(name):
    """Return a fresh copy of one table as a pandas DataFrame."""
    if name not in _CACHE:
        _CACHE[name] = _read(name)
    return _CACHE[name].copy()


def tables():
    """Names of the tables you can load."""
    return sorted(f[:-8] for f in os.listdir(PARQUET_DIR) if f.endswith(".parquet"))
