# ============================================================================================
# 02_numpy  |  Q08  |  ★★★ challenge
#
# Put every live loan at 2025-12-31 into a tier with `np.select` on `days_past_due`: 0 =
# `'Current'`, 1-29 = `'Early'`, 30-89 = `'Late'`, 90+ = `'Default'`. Return `tier`,
# `loans`; sorted by `tier`.
#
# Return 2 column(s), in the order the question gives them. Expected 4 row(s).
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
d = live['days_past_due']
tier = np.select([d == 0, d < 30, d < 90], ['Current', 'Early', 'Late'], default='Default')
result = pd.Series(tier).value_counts().sort_index()
