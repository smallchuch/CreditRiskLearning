# ============================================================================================
# 03_selection  |  Q06  |  ★★ core
#
# Sort `loan` by `original_amount` (largest first), then `loan_id`. What is the `loan_id` of
# the **100th** row (position 99)?
#
# Return 1 column(s), in the order the question gives them. Expected 1 row(s).
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
result = int(loan.sort_values(['original_amount', 'loan_id'], ascending=[False, True]).iloc[99]['loan_id'])
