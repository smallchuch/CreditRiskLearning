# ============================================================================================
# 02_numpy  |  Q04  |  ★★ core
#
# The 10th, 50th and 90th percentiles of `original_amount` (`np.percentile`), as a list of
# three numbers rounded to 0 dp, in that order.
#
# Return 1 column(s), in the order the question gives them. Expected 3 row(s).
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
