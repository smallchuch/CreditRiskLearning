# ============================================================================================
# 05_missing_strings  |  Q06  |  ★★ core
#
# On `applicant_income`, use the verified amount where there is one and the declared amount
# otherwise (`fillna` from another column). Return the total annual income across all lines,
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

applicant_income = load('applicant_income')

# %% your answer
amount = applicant_income['verified_annual_amount'].fillna(applicant_income['declared_annual_amount'])
result = round(amount.sum(), 0)
