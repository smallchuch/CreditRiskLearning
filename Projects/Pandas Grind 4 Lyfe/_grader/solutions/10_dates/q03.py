# ============================================================================================
# 10_dates  |  Q03  |  ★ warm-up
#
# Median number of days from `application_date` to `decision_date` for **approved**
# applications. Return a number.
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

app = load('loan_application')

# %% your answer
a = app[app['decision'] == 'Approved']
result = float((a['decision_date'] - a['application_date']).dt.days.median())
