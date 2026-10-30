# ============================================================================================
# 05_missing_strings  |  Q05  |  ★★ core
#
# Each customer's age in **whole years** (rounded down) at 2025-12-31, from `date_of_birth`.
# Customers without a date of birth are left out. Return the average age, rounded to 1 dp.
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

customer = load('customer')

# %% your answer
asat = pd.Timestamp('2025-12-31')
dob = customer['date_of_birth'].dropna()
age = asat.year - dob.dt.year - (dob.dt.strftime('%m%d') > asat.strftime('%m%d')).astype(int)
result = round(age.mean(), 1)
