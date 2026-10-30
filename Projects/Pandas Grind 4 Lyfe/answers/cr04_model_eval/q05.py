# ============================================================================================
# cr04_model_eval  |  Q05  |  ★★★ challenge
#
# Stability: the Gini of the bureau score for each origination year 2019 to 2024, rounded to
# 4 dp, computed in a loop. Return `year`, `gini`; sorted by `year`.
#
# Return 2 column(s), in the order the question gives them. Expected 6 row(s).
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
applicant = load('application_applicant')
bureau = load('credit_bureau_report')
loan = load('loan')

# %% your answer
result = None
