# ============================================================================================
# 11_shift_cumulative  |  Q06  |  ★★ core
#
# Roll forward: how many loans were 30-59 days past due at 2025-11-30 **and** 60-89 days
# past due at 2025-12-31?
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
nov = snap.loc[snap['snapshot_date'] == '2025-11-30', ['loan_id', 'days_past_due']]
dec = snap.loc[snap['snapshot_date'] == '2025-12-31', ['loan_id', 'days_past_due']]
m = nov.merge(dec, on='loan_id', suffixes=('_nov', '_dec'))
result = int((m['days_past_due_nov'].between(30, 59) & m['days_past_due_dec'].between(60, 89)).sum())
