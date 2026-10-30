# ============================================================================================
# 09_binning  |  Q05  |  ★★ core
#
# Live loans at 2025-12-31 split into 5 equal-count groups on `days_past_due`. Plain `qcut`
# fails (most values are 0), so `qcut` the `rank(method='first')` instead. Groups numbered 1
# to 5. Return `group`, `n`, `max_dpd`; sorted by `group`.
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
