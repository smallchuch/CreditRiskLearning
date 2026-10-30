# ============================================================================================
# cr01_portfolio  |  Q02  |  ★ warm-up
#
# Live balance share by `purpose` (join from `loan`), as a percentage rounded to 2 dp.
# Return `purpose`, `balance_pct`; sorted by `balance_pct` (largest first).
#
# Return 2 column(s), in the order the question gives them. Expected 6 row(s).
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
loan = load('loan')

# %% your answer
result = None
