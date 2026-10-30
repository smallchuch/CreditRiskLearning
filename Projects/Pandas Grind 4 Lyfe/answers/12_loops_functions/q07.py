# ============================================================================================
# 12_loops_functions  |  Q07  |  ★★★ challenge
#
# A comprehension instead of a loop: for live loans at 2025-12-31, the percentage with
# `days_past_due` at or above each threshold in `[1, 30, 60, 90]`, rounded to 3 dp. Return
# `threshold`, `pct`; sorted by `threshold`.
#
# Return 2 column(s), in the order the question gives them. Expected 4 row(s).
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
