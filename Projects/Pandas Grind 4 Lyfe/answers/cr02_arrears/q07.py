# ============================================================================================
# cr02_arrears  |  Q07  |  ★★★ challenge
#
# A 12-month cohort default rate. Cohort = live loans at 2024-12-31 that were **current** (0
# days past due) then. Bad = reached 90+ days past due at **any** 2025 month-end. Return one
# row: `cohort`, `bads`, `default_rate_pct` (3 dp).
#
# Return 3 column(s), in the order the question gives them. Expected 1 row(s).
# Row order does not matter.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

snap = load('loan_monthly_snapshot')

# %% your answer
result = None
