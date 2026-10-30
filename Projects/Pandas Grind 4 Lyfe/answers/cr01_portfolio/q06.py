# ============================================================================================
# cr01_portfolio  |  Q06  |  ★★ core
#
# Live balance in $ millions (1 dp) by `occupancy` (rows, from `dim_product` via `loan`) and
# the snapshot's `repayment_type` (columns). Return `occupancy`, `Interest Only`, `P&I`;
# sorted by `occupancy`.
#
# Return 3 column(s), in the order the question gives them. Expected 2 row(s).
# Sort the output as described.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

snap = load('loan_monthly_snapshot')
loan = load('loan')
dim_product = load('dim_product')

# %% your answer
result = None
