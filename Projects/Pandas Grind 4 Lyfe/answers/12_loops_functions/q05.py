# ============================================================================================
# 12_loops_functions  |  Q05  |  ★★ core
#
# Write `summarise(df, by, col='original_amount')` returning, per group of `by`, `n` (rows)
# and `mean` (mean of `col`, rounded to 0 dp). Call it with `by='purpose'`, leaving `col` at
# its default. Return `purpose`, `n`, `mean`; sorted by `purpose`.
#
# Return 3 column(s), in the order the question gives them. Expected 6 row(s).
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
