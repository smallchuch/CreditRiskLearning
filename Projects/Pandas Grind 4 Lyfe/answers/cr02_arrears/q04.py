# ============================================================================================
# cr02_arrears  |  Q04  |  ★★★ challenge
#
# Roll-rate matrix November -> December 2025 for loans that are live (not `'Closed'`) in
# **both** month-end snapshots. Buckets `Current`, `1-29`, `30-59`, `60-89`, `90+`; **row
# percentages** rounded to 2 dp, 0 where nothing rolled. Return `from_bucket` then one
# column per December bucket in bucket order; rows in bucket order.
#
# Return 6 column(s), in the order the question gives them. Expected 5 row(s).
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

# %% your answer
result = None
