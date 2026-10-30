# ============================================================================================
# 06_groupby  |  Q09  |  ★★★ challenge
#
# The single largest loan in each `purpose` (ties: smaller `loan_id` wins). Return
# `purpose`, `loan_id`, `original_amount`; sorted by `purpose`.
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
