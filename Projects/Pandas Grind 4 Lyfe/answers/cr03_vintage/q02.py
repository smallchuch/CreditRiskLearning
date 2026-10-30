# ============================================================================================
# cr03_vintage  |  Q02  |  ★★ core
#
# Cumulative ever-90 rate **by MOB 12** for vintages 2019 to 2024: the percentage of each
# vintage's loans whose first 90+ month-end came at `months_on_book <= 12`. Denominator =
# all loans in the vintage. Return `vintage`, `pct` (2 dp); sorted by `vintage`.
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
