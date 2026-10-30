# ============================================================================================
# 09_binning  |  Q08  |  ★★ core
#
# Histogram as a table: live loans at 2025-12-31 binned by `interest_rate_pct` into
# 0.5-point bins from 4.0 to 9.0 (left-closed; anything outside is dropped). Return
# `bin_start`, `loans` for bins with loans, where `bin_start` is the lower edge as a number
# (e.g. 4.0); sorted by `bin_start`.
#
# Return 2 column(s), in the order the question gives them. Expected 7 row(s).
# Sort the output as described.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

snap = load('loan_monthly_snapshot')

# %% your answer
live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')]

edges = np.arange(4.0, 9.01, 0.5)
b = pd.cut(live['interest_rate_pct'], bins=edges, right=False, labels=edges[:-1])
result = b.value_counts(sort=False)
result = result[result > 0].rename_axis('bin_start')
result.index = result.index.astype(float)
