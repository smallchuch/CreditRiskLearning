# ============================================================================================
# 04_index_alignment  |  Q01  |  ★ warm-up
#
# Using `set_index('loan_id')` and `.loc`, return the `original_amount` of loan 12345.
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
result = loan.set_index('loan_id').loc[12345, 'original_amount']
