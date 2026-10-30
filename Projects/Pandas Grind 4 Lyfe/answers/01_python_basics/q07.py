# ============================================================================================
# 01_python_basics  |  Q07  |  ★★ core
#
# Write a function `pct_above(series, cut)` that returns the **percentage** of values
# strictly above `cut` (ignore missing values in the denominator). Use it for
# `lvr_at_origination_pct` at cuts 60, 70, 80, 90 and 95. Return `cut`, `pct` (rounded to 2
# dp); sorted by `cut`.
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

loan = load('loan')

# %% your answer
result = None
