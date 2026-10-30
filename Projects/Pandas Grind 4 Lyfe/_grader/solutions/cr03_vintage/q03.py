# ============================================================================================
# cr03_vintage  |  Q03  |  ★★★ challenge
#
# The full vintage table: rows = vintages 2019 to 2023, columns = MOB 6, 12, 18, 24, values
# = cumulative ever-90 % by that MOB (2 dp). Return `vintage`, `6`, `12`, `18`, `24`; sorted
# by `vintage`.
#
# Return 5 column(s), in the order the question gives them. Expected 5 row(s).
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

v = v[v['vintage'].between(2019, 2023)]
cols = {}
for m in [6, 12, 18, 24]:
    cols[m] = (100 * (v['first90_mob'] <= m).groupby(v['vintage']).mean()).round(2)
result = pd.DataFrame(cols).rename_axis('vintage')
