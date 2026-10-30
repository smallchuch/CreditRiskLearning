# ============================================================================================
# 07_merge  |  Q04  |  ★★ core
#
# Fan-out check. Join `loan` to `loan_security` on `loan_id` (inner). Return one row:
# `rows_before` (loans), `rows_after` (rows after the join) and `amount_double_counted` =
# the sum of `original_amount` after the join minus the true total, rounded to 0 dp.
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

loan = load('loan')
loan_security = load('loan_security')

# %% your answer
result = None
