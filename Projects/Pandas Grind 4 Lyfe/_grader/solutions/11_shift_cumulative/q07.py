# ============================================================================================
# 11_shift_cumulative  |  Q07  |  ★★★ challenge
#
# Ever-90 by vintage: flag each loan that **ever** reached 90+ days past due, then per
# origination year return `year`, `loans`, `ever90`, `ever90_pct` (2 dp); sorted by `year`.
#
# Return 4 column(s), in the order the question gives them. Expected 8 row(s).
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
ever = (snap.groupby('loan_id')['days_past_due'].max() >= 90).rename('ever90')
l = loan[['loan_id', 'origination_date']].merge(ever, left_on='loan_id', right_index=True, how='left')
l['ever90'] = l['ever90'].fillna(False).astype(int)
result = l.groupby(l['origination_date'].dt.year.rename('year')).agg(loans=('ever90', 'size'), ever90=('ever90', 'sum'))
result['ever90_pct'] = (100 * result['ever90'] / result['loans']).round(2)
