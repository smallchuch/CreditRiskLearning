# ============================================================================================
# cr04_model_eval  |  Q01  |  ★ warm-up
#
# Build the population (see the primer; thin files dropped). Return one row: `loans`,
# `bads`, `bad_rate_pct` (3 dp).
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
applicant = load('application_applicant')
bureau = load('credit_bureau_report')
loan = load('loan')

# %% your answer
result = None
