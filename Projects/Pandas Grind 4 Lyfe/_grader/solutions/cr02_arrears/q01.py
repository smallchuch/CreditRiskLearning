# ============================================================================================
# cr02_arrears  |  Q01  |  ★ warm-up
#
# The **30+ arrears rate by count** of the live book at each month-end of 2025 (live = not
# `'Closed'` that month), as a percentage rounded to 3 dp. Month as `'2025-01'` etc. Return
# `month`, `pct_30plus`; sorted by `month`.
#
# Return 2 column(s), in the order the question gives them. Expected 12 row(s).
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
s = snap[(snap['snapshot_date'].dt.year == 2025) & (snap['loan_status'] != 'Closed')]
r = 100 * (s['days_past_due'] >= 30).groupby(s['snapshot_date'].dt.strftime('%Y-%m').rename('month')).mean()
result = r.round(3)
