# ============================================================================================
# 10_dates  |  Q02  |  ★ warm-up
#
# Loans originated per month of 2025, with the month as a string like `'2025-03'`. Return
# `month`, `loans`; sorted by `month`.
#
# Return 2 column(s), in the order the question gives them. Expected 12 row(s).
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
l = loan[loan['origination_date'].dt.year == 2025]
result = l['origination_date'].dt.to_period('M').astype(str).value_counts().sort_index().rename_axis('month')
