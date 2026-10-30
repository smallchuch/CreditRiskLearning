# ============================================================================================
# 03_selection  |  Q05  |  ★★ core
#
# Active loans (`loan_status == 'Active'`) with `lvr_at_origination_pct` above 98. Return
# `loan_id`, `lvr_at_origination_pct`; sorted by `loan_id`.
#
# Return 2 column(s), in the order the question gives them. Expected 209 row(s).
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
mask = (loan['loan_status'] == 'Active') & (loan['lvr_at_origination_pct'] > 98)
result = loan.loc[mask, ['loan_id', 'lvr_at_origination_pct']].sort_values('loan_id')
