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
result = None
