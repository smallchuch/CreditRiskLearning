# ============================================================================================
# cr03_vintage  |  Q05  |  ★★★ challenge
#
# **Balance-weighted** cumulative ever-90 by MOB 24 for vintages 2019 to 2023: original
# amount of loans that went 90+ by MOB 24 / original amount of the whole vintage, as % (2
# dp). Return `vintage`, `pct_by_amount`; sorted by `vintage`.
#
# Return 2 column(s), in the order the question gives them. Expected 5 row(s).
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
loan = load('loan')

# %% your answer
first90 = snap[snap['days_past_due'] >= 90].groupby('loan_id')['months_on_book'].min().rename('first90_mob')
v = loan[['loan_id', 'origination_date', 'original_amount']].merge(first90, left_on='loan_id', right_index=True, how='left')
v['vintage'] = v['origination_date'].dt.year

v = v[v['vintage'].between(2019, 2023)].copy()
v['bad_amt'] = v['original_amount'].where(v['first90_mob'] <= 24, 0)
g = v.groupby('vintage')[['bad_amt', 'original_amount']].sum()
result = (100 * g['bad_amt'] / g['original_amount']).round(2)
