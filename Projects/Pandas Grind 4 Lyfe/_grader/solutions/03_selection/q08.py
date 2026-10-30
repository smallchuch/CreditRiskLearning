# ============================================================================================
# 03_selection  |  Q08  |  ★★★ challenge
#
# Among **Variable**-rate loans originated in **2025**, the 10 with the highest
# `interest_rate_at_origination_pct`. Return `loan_id`, `interest_rate_at_origination_pct`;
# sorted by rate (highest first), then `loan_id`.
#
# Return 2 column(s), in the order the question gives them. Expected 10 row(s).
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
mask = (loan['rate_type'] == 'Variable') & (loan['origination_date'].dt.year == 2025)
cols = ['loan_id', 'interest_rate_at_origination_pct']
result = (loan.loc[mask, cols]
          .sort_values(['interest_rate_at_origination_pct', 'loan_id'], ascending=[False, True])
          .head(10))
