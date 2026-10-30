# ============================================================================================
# cr02_arrears  |  Q03  |  ★★ core
#
# Live loans and balance by arrears bucket at 2025-12-31 with buckets `'Current'` (0),
# `'1-29'`, `'30-59'`, `'60-89'`, `'90+'`. Return `bucket`, `loans`, `balance_m` (2 dp) in
# bucket order.
#
# Return 3 column(s), in the order the question gives them. Expected 5 row(s).
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
order = ['Current', '1-29', '30-59', '60-89', '90+']
def bucket(dpd):
    return pd.Categorical(pd.cut(dpd, [-1, 0, 29, 59, 89, np.inf], labels=order), categories=order, ordered=True)

live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')].copy()
live['bucket'] = bucket(live['days_past_due'])
g = live.groupby('bucket', observed=False).agg(loans=('loan_id', 'size'), balance_m=('closing_balance', 'sum'))
g['balance_m'] = (g['balance_m'] / 1e6).round(2)
result = g
