# ============================================================================================
# 07_merge  |  Q02  |  ★ warm-up
#
# Join `app` to `assess` on `application_id` and return the median `nsr` for `'Approved'`
# and `'Declined'` decisions, rounded to 3 dp. Return `decision`, `median_nsr`; sorted by
# `decision`.
#
# Return 2 column(s), in the order the question gives them. Expected 2 row(s).
# Sort the output as described.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

app = load('loan_application')
assess = load('application_assessment')

# %% your answer
result = None
