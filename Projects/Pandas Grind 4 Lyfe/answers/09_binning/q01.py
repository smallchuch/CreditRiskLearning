# ============================================================================================
# 09_binning  |  Q01  |  ★ warm-up
#
# Band every loan's `lvr_at_origination_pct` with `pd.cut` using the `ref_lvr_band` edges 0,
# 60, 70, 80, 90, 95, inf (left-closed) and labels `'<= 60%'`, `'60-70%'`, `'70-80%'`,
# `'80-90%'`, `'90-95%'`, `'> 95%'`. Return `band`, `loans` in band order (lowest first).
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

loan = load('loan')

# %% your answer
result = None
