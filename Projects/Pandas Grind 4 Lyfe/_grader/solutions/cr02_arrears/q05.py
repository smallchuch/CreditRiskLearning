# ============================================================================================
# cr02_arrears  |  Q05  |  ★★ core
#
# Cure rate: of the loans 30+ days past due at 2025-06-30, what percentage were back to 0
# days past due at 2025-12-31? Denominator = those 30+ at June that still have a December
# snapshot. Round to 2 dp.
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
jun = snap.loc[(snap['snapshot_date'] == '2025-06-30') & (snap['days_past_due'] >= 30), ['loan_id']]
dec = snap.loc[snap['snapshot_date'] == '2025-12-31', ['loan_id', 'days_past_due']]
m = jun.merge(dec, on='loan_id')
result = round(100 * (m['days_past_due'] == 0).mean(), 2)
