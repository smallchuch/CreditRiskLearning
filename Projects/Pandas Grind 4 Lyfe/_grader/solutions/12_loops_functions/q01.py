# ============================================================================================
# 12_loops_functions  |  Q01  |  ★ warm-up
#
# Loop over the four channels and compute the percentage of each channel's loans that are
# `'Closed'`, storing results in a dict. Return `channel`, `pct_closed` (2 dp); sorted by
# `channel`.
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

loan = load('loan')

# %% your answer
out = {}
for ch in sorted(loan['channel'].unique()):
    sub = loan[loan['channel'] == ch]
    out[ch] = round(100 * (sub['loan_status'] == 'Closed').mean(), 2)
result = pd.Series(out, name='pct_closed').rename_axis('channel')
