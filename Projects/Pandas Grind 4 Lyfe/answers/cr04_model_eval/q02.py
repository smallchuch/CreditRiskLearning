# ============================================================================================
# cr04_model_eval  |  Q02  |  ★★ core
#
# Score deciles: `rank(method='first')` on `bureau_score`, `qcut` into 10, numbered 1
# (lowest scores) to 10. Return `decile`, `loans`, `bads`, `bad_rate_pct` (2 dp); sorted by
# `decile`.
#
# Return 4 column(s), in the order the question gives them. Expected 10 row(s).
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
