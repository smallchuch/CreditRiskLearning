# ============================================================================================
# 10_dates  |  Q07  |  ★★ core
#
# Total book balance (`closing_balance` of all rows, $ millions, 2 dp) at each **2025
# quarter-end** snapshot (31 Mar, 30 Jun, 30 Sep, 31 Dec). Return `quarter_end` (as
# `'2025-03-31'` etc.), `balance_m`; sorted by `quarter_end`.
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
