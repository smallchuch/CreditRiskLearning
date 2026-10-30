# ============================================================================================
# 01_python_basics  |  Q04  |  ★ warm-up
#
# The number of loans originated in each calendar year, as a dict `{year: loans}` built
# **with a loop** (no groupby). Years are ints.
#
# Return 2 column(s), in the order the question gives them. Expected 8 row(s).
# Row order does not matter.
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
counts = {}
for y in loan['origination_date'].dt.year:
    counts[int(y)] = counts.get(int(y), 0) + 1
result = counts
