# ============================================================================================
# 09_binning  |  Q07  |  ★★★ challenge
#
# Percentile rank of each live loan's `closing_balance` at 2025-12-31 (`rank(pct=True)`).
# How many loans sit in the top 1% (percentile rank of 0.99 or more)?
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

snap = load('loan_monthly_snapshot')

# %% your answer
live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')]

result = int((live['closing_balance'].rank(pct=True) >= 0.99).sum())
