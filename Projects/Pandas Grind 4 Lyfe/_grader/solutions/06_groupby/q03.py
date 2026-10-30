# ============================================================================================
# 06_groupby  |  Q03  |  ★ warm-up
#
# Per `rate_type`, with named aggregation: `loans` (count), `total_amount` (sum of
# `original_amount`, rounded to 0 dp) and `avg_lvr` (mean `lvr_at_origination_pct`, rounded
# to 2 dp). Return `rate_type`, `loans`, `total_amount`, `avg_lvr`; sorted by `rate_type`.
#
# Return 4 column(s), in the order the question gives them. Expected 2 row(s).
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
result = loan.groupby('rate_type').agg(loans=('loan_id', 'size'),
                                       total_amount=('original_amount', 'sum'),
                                       avg_lvr=('lvr_at_origination_pct', 'mean'))
result['total_amount'] = result['total_amount'].round(0)
result['avg_lvr'] = result['avg_lvr'].round(2)
