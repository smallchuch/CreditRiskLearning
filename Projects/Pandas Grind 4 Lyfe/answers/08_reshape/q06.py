# ============================================================================================
# 08_reshape  |  Q06  |  ★★★ challenge
#
# Start from the year x `rate_type` count table (Q01), `stack` it back to long form and keep
# only cells with **more than 2,000** loans. Return `year`, `rate_type`, `loans`; sorted by
# `year`, `rate_type`.
#
# Return 3 column(s), in the order the question gives them. Expected 9 row(s).
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
