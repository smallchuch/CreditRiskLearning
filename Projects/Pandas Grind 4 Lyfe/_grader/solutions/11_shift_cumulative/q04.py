# ============================================================================================
# 11_shift_cumulative  |  Q04  |  ★★ core
#
# New loans per month in 2025 and their **3-month rolling average** (rounded to 1 dp; the
# first two months are missing). Month as `'2025-01'` etc. Return `month`, `loans`,
# `rolling_3m`; sorted by `month`.
#
# Return 3 column(s), in the order the question gives them. Expected 12 row(s).
# Sort the output as described.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

loan = load('loan')

# %% your answer
l = loan[loan['origination_date'].dt.year == 2025]
n = l['origination_date'].dt.to_period('M').astype(str).value_counts().sort_index()
result = pd.DataFrame({'loans': n, 'rolling_3m': n.rolling(3).mean().round(1)}).rename_axis('month')
