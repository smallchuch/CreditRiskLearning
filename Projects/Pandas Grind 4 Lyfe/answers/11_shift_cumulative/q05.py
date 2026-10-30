# ============================================================================================
# 11_shift_cumulative  |  Q05  |  ★★ core
#
# New arrears: count the loan-months in **2025** where `days_past_due` was 0 the month
# before and above 0 this month. Use a **grouped** `shift` so one loan never borrows another
# loan's history.
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

# %% your answer
result = None
