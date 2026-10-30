# ============================================================================================
# 05_missing_strings  |  Q09  |  ★★★ challenge
#
# A few `loan_rate_history` rates were keyed as fractions (`0.0629` instead of `6.29`). Find
# them (rate below 1), fix them by multiplying by 100, and return one row: `n_fixed`,
# `mean_before`, `mean_after` (means rounded to 4 dp).
#
# Return 3 column(s), in the order the question gives them. Expected 1 row(s).
# Row order does not matter.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

loan_rate_history = load('loan_rate_history')

# %% your answer
r = loan_rate_history['interest_rate_pct'].copy()
bad = r < 1
before = r.mean()
r[bad] = r[bad] * 100
result = pd.DataFrame({'n_fixed': [int(bad.sum())], 'mean_before': [round(before, 4)], 'mean_after': [round(r.mean(), 4)]})
