# ============================================================================================
# cr05_origination  |  Q05  |  ★★ core
#
# Recompute the surplus: `assessed_net_monthly_income - assessed_living_expenses -
# assessed_commitments_monthly - new_loan_assessed_repayment`. How many applications differ
# from the stored `monthly_surplus` by more than $1?
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

assess = load('application_assessment')

# %% your answer
result = None
