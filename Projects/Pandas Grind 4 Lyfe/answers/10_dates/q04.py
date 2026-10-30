# ============================================================================================
# 10_dates  |  Q04  |  ★★ core
#
# For live loans at 2025-12-31, the remaining term in **whole months** from 2025-12 to the
# `maturity_date` month (join `maturity_date` from `loan`). Return the average, rounded to 1
# dp.
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
loan = load('loan')

# %% your answer
result = None
