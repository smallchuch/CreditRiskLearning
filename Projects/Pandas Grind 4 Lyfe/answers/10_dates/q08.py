# ============================================================================================
# 10_dates  |  Q08  |  ★★★ challenge
#
# Snapshot gaps: a loan should have one row for every month from MOB 0 to its last MOB.
# Count the loans whose number of snapshot rows is **not** equal to `max(months_on_book) +
# 1`.
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
