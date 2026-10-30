# ============================================================================================
# 02_numpy  |  Q07  |  ★★ core
#
# Balance-weighted average `interest_rate_pct` of the **live book** at 2025-12-31
# (`snapshot_date` = 2025-12-31 and `loan_status` not `'Closed'`), weights =
# `closing_balance`. Use `np.average`. Round to 3 dp.
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
live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')]
result = round(np.average(live['interest_rate_pct'], weights=live['closing_balance']), 3)
