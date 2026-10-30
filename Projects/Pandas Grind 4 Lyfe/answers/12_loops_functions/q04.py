# ============================================================================================
# 12_loops_functions  |  Q04  |  ★★ core
#
# Vectorised maths, no row loop: the P&I monthly repayment for each loan is `P * r / (1 - (1
# + r) ** -n)` with `P = original_amount`, `r = interest_rate_at_origination_pct / 1200`, `n
# = term_months`. Return the **total** of these repayments for loans originated in 2025,
# rounded to 0 dp.
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
result = None
