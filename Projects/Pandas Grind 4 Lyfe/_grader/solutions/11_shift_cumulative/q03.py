# ============================================================================================
# 11_shift_cumulative  |  Q03  |  ★★ core
#
# Year-on-year growth in the number of loans originated, as a percentage rounded to 1 dp
# (`pct_change`). Return `year`, `growth_pct`; sorted by `year` (the first year is missing).
#
# Return 2 column(s), in the order the question gives them. Expected 8 row(s).
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
n = loan['origination_date'].dt.year.value_counts().sort_index()
result = (n.pct_change() * 100).round(1).rename_axis('year')
