# ============================================================================================
# cr03_vintage  |  Q06  |  ★★★ challenge
#
# Survival: for vintages 2019 to 2023, the percentage of each vintage's loans that still had
# a non-`'Closed'` snapshot at MOB 24. Return `vintage`, `pct_open_mob24` (2 dp); sorted by
# `vintage`.
#
# Return 2 column(s), in the order the question gives them. Expected 5 row(s).
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
