"""Stage 00: read raw orig/perf files for one year straight from the zip, trim columns, save Parquet."""

import zipfile

import pandas as pd

from freddie.config import ORIG_COLS, ORIG_DTYPES, PERF_COLS, PERF_DTYPES, PERF_KEEP, RAW_DIR, INTERIM_DIR

# Loan Origination Data
def load_orig(year, save=False):                      # save defaults to off
    """Load the origination file for one year from the raw zip.

    One row per loan, with the traits recorded at approval (credit score,
    LTV, DTI, rate, purpose, and so on). Column names and dtypes come from
    ``ORIG_COLS`` and ``ORIG_DTYPES`` in config.

    Parameters
    ----------
    year : int
        Origination year of the sample file, e.g. 2007.
    save : bool, default False
        If True, also write the frame to ``INTERIM_DIR/orig_<year>.parquet``.

    Returns
    -------
    pandas.DataFrame
        About 50,000 rows x 31 columns.
    """
    zip_path = RAW_DIR / f"sample_{year}.zip"

    with zipfile.ZipFile(zip_path) as z:
        with z.open(f"sample_orig_{year}.txt") as f:
            orig = pd.read_csv(
                f,
                sep="|",
                header=None,
                names=ORIG_COLS,                      # from config
                dtype=ORIG_DTYPES,                    # from config
            )

    print(f"{year} orig: {orig.shape[0]:,} rows x {orig.shape[1]} cols")  # one-line log

    if save:                                          # only runs when save=True
        out_path = INTERIM_DIR / f"orig_{year}.parquet"
        orig.to_parquet(out_path, index=False)
        print(f"saved -> {out_path.name}")

    return orig                                       # always hand back the DataFrame
    
        
    # Monthly loan performance data
def load_perf(year, save=False):
    """Load the monthly performance file for one year from the raw zip.

    One row per loan per month, from first reporting until the loan closes
    or the data ends. Only the columns in ``PERF_KEEP`` are read, which keeps
    a year to roughly 3 million rows x 7 columns.

    Parameters
    ----------
    year : int
        Origination year of the sample file, e.g. 2007.
    save : bool, default False
        If True, also write the frame to ``INTERIM_DIR/perf_<year>.parquet``.

    Returns
    -------
    pandas.DataFrame
        Loan-month panel with loan_id, period, balance, delinquency status,
        loan age and zero balance fields.
    """
    
    zip_path = RAW_DIR / f"sample_{year}.zip"
    
    with zipfile.ZipFile(zip_path) as z:
        with z.open(f"sample_perf_{year}.txt") as f:
            perf = pd.read_csv(
                f,
                sep="|",
                header=None,
                names=PERF_COLS,                              
                usecols=PERF_KEEP,                             # just the ones you need
                dtype={c: PERF_DTYPES[c] for c in PERF_KEEP},
                
            )
    
    if save:                                          # only runs when save=True
        out_path = INTERIM_DIR / f"perf_{year}.parquet"
        perf.to_parquet(out_path, index=False)
        print(f"saved -> {out_path.name}")
    
    return perf
        
    # Sanity Check
    
def sanity_check(year):
    """Print the shapes of the saved interim files for one year.

    A quick size check that both Parquet files exist and have the expected
    number of rows (about 50,000 orig, about 3 million perf).

    Parameters
    ----------
    year : int
        Origination year to check.
    """

    orig = pd.read_parquet(INTERIM_DIR / f"orig_{year}.parquet")   # one row per loan
    perf = pd.read_parquet(INTERIM_DIR / f"perf_{year}.parquet")   # one row per loan per month

    print(orig.shape, perf.shape)   # expect ~50k rows, and ~3m once you've removed nrows