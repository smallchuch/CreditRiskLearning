# ============================================================================================
# cr03_vintage  |  Q02  |  ★★ core
#
# Cumulative ever-90 rate **by MOB 12** for vintages 2019 to 2024: the percentage of each
# vintage's loans whose first 90+ month-end came at `months_on_book <= 12`. Denominator =
# all loans in the vintage. Return `vintage`, `pct` (2 dp); sorted by `vintage`.
#
# Return 2 column(s), in the order the question gives them. Expected 6 row(s).
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

v = v[v['vintage'].between(2019, 2024)]
result = (100 * (v['first90_mob'] <= 12).groupby(v['vintage']).mean()).round(2)
