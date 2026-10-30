# ============================================================================================
# cr01_portfolio  |  Q01  |  ★ warm-up
#
# Live book at 2025-12-31: number of loans and total balance in **$ millions** (2 dp).
# Return one row: `loans`, `balance_m`.
#
# Return 2 column(s), in the order the question gives them. Expected 1 row(s).
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
