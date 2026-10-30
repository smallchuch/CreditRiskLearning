# ============================================================================================
# 08_reshape  |  Q01  |  ★ warm-up
#
# Loans by origination year (rows) and `rate_type` (columns) with `pivot_table`. Return
# `year`, `Fixed`, `Variable`; sorted by `year`.
#
# Return 3 column(s), in the order the question gives them. Expected 8 row(s).
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
