# ============================================================================================
# 02_numpy  |  Q06  |  ★★ core
#
# For `loan_id` 1664 (a variable-rate loan from 2019), take its `interest_rate_pct` month by
# month (`snap`, ordered by `snapshot_date`). How many month-to-month steps were **rate
# rises**? Use `np.diff` and `np.sign`.
#
# Return 1 column(s), in the order the question gives them. Expected 1 row(s).
# Row order does not matter.
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
rates = snap.loc[snap['loan_id'] == 1664].sort_values('snapshot_date')['interest_rate_pct'].to_numpy()
result = int((np.sign(np.diff(rates)) == 1).sum())
