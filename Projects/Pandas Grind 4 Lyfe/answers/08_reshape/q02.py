# ============================================================================================
# 08_reshape  |  Q02  |  ★ warm-up
#
# `pd.crosstab` of `channel` (rows) by `rate_type` (columns) as **row percentages** rounded
# to 2 dp. Return `channel`, `Fixed`, `Variable`; sorted by `channel`.
#
# Return 3 column(s), in the order the question gives them. Expected 4 row(s).
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
