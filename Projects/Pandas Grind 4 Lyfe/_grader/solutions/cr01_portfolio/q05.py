# ============================================================================================
# cr01_portfolio  |  Q05  |  ★★ core
#
# Live balance by **origination LVR band** (`ref_lvr_band` edges, left-closed: `<= 60%`,
# `60-70%`, `70-80%`, `80-90%`, `90-95%`, `> 95%`). Return `band`, `balance_m` (2 dp),
# `balance_pct` (2 dp) in band order.
#
# Return 3 column(s), in the order the question gives them. Expected 6 row(s).
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
live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')]

m = live[['loan_id', 'closing_balance']].merge(loan[['loan_id', 'lvr_at_origination_pct']], on='loan_id')
labels = ['<= 60%', '60-70%', '70-80%', '80-90%', '90-95%', '> 95%']
m['band'] = pd.cut(m['lvr_at_origination_pct'], [0, 60, 70, 80, 90, 95, np.inf], right=False, labels=labels)
bal = m.groupby('band', observed=False)['closing_balance'].sum()
result = pd.DataFrame({'balance_m': (bal / 1e6).round(2), 'balance_pct': (100 * bal / bal.sum()).round(2)})
