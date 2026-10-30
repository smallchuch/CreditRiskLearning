# ============================================================================================
# 01_python_basics  |  Q06  |  ★★ core
#
# Each rule below is `name: (column, threshold)`. Loop over the dict and count the loans
# where the column is **strictly above** the threshold. Return `rule`, `loans`; sorted by
# `rule`.
#
# ```python
# rules = {
#     'big_loan':  ('original_amount', 1_000_000),
#     'high_lvr':  ('lvr_at_origination_pct', 90),
#     'high_rate': ('interest_rate_at_origination_pct', 7),
# }
# ```
#
# Return 2 column(s), in the order the question gives them. Expected 3 row(s).
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
