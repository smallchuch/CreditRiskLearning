# ============================================================================================
# 10_dates  |  Q05  |  ★★ core
#
# Loans originated per **Australian financial year** (FY ends 30 June; FY2025 = Jul 2024 -
# Jun 2025). Return `fy`, `loans`; sorted by `fy`.
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
d = loan['origination_date']
fy = d.dt.year + (d.dt.month >= 7).astype(int)
result = fy.value_counts().sort_index().rename_axis('fy')
