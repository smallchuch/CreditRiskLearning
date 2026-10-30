# ============================================================================================
# 07_merge  |  Q07  |  ★★★ challenge
#
# For each loan, find the **RBA cash rate in force** at its `origination_date` (latest
# `bank_effective_date` on or before it, `merge_asof`). Average spread =
# `interest_rate_at_origination_pct` minus `cash_rate_pct`, per origination year, rounded to
# 3 dp. Return `year`, `avg_spread`; sorted by `year`.
#
# Return 2 column(s), in the order the question gives them. Expected 8 row(s).
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
ref_rba_cash_rate = load('ref_rba_cash_rate')

# %% your answer
result = None
