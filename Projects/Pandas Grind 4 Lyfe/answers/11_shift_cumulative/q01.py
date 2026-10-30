# ============================================================================================
# 11_shift_cumulative  |  Q01  |  ★ warm-up
#
# For `loan_id` 1664, the month-to-month change in `closing_balance` (sorted by
# `snapshot_date`, `diff`). What was the **largest single monthly reduction**, as a positive
# number rounded to 2 dp?
#
# Return 1 column(s), in the order the question gives them. Expected 1 row(s).
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
