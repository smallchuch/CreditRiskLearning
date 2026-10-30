# ============================================================================================
# 05_missing_strings  |  Q01  |  ★ warm-up
#
# Which columns of `loan` have missing values, and how many? Return `column`, `n_missing`
# for columns with at least one missing value; sorted by `column`.
#
# Return 2 column(s), in the order the question gives them. Expected 9 row(s).
# Sort the output as described.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

loan = load('loan')

# %% your answer
n = loan.isna().sum()
result = n[n > 0].rename_axis('column').sort_index()
