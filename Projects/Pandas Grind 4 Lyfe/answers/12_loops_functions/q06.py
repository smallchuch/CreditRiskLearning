# ============================================================================================
# 12_loops_functions  |  Q06  |  ★★★ challenge
#
# Compare "models" the notebook-03 way. Population: loans with an application, the primary
# applicant's bureau score (thin files dropped) and the application's `assess` row. Outcome
# `bad` = the loan ever reached 90+ days past due. Three single-variable "models", each a
# risk score where **higher = riskier**:
#
# ```python
# models = {'bureau_score': -df['bureau_score'], 'nsr': -df['nsr'], 'dti_ratio': df['dti_ratio']}
# ```
#
# Loop over the dict and compute each Gini (`2 * roc_auc_score(bad, score) - 1`). Return
# `model`, `gini` (4 dp); sorted by `gini` (highest first).
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

snap = load('loan_monthly_snapshot')
applicant = load('application_applicant')
bureau = load('credit_bureau_report')
loan = load('loan')
assess = load('application_assessment')

# %% your answer
result = None
