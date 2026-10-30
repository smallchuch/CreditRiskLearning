# ============================================================================================
# cr05_origination  |  Q01  |  ★ warm-up
#
# Decline rate (% of decided applications that were declined, 2 dp) by **application month**
# of 2025, month as `'2025-01'`. Return `month`, `decline_pct`; sorted by `month`.
#
# Return 2 column(s), in the order the question gives them. Expected 12 row(s).
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

# %% your answer
d = app[(app['application_date'].dt.year == 2025) & app['decision'].notna()]
result = (100 * (d['decision'] == 'Declined').groupby(d['application_date'].dt.strftime('%Y-%m').rename('month')).mean()).round(2)
