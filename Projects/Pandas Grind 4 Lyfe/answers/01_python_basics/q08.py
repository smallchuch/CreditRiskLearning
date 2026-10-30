# ============================================================================================
# 01_python_basics  |  Q08  |  ★★★ challenge
#
# Build a nested dict `{purpose: {'loans': n, 'avg_amount': mean}}` with a loop over the
# purposes, then turn it into a table. Return `purpose`, `loans`, `avg_amount` (rounded to 0
# dp); sorted by `purpose`.
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
