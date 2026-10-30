# ============================================================================================
# cr05_origination  |  Q06  |  ★★ core
#
# Settled loans with a DTI above 6 (`assess.dti_ratio > 6`), as a % of settled applications
# per application year 2019 to 2025 (2 dp). Return `year`, `dti6_pct`; sorted by `year`.
#
# Return 2 column(s), in the order the question gives them. Expected 7 row(s).
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
s = app.loc[app['current_status'] == 'Settled', ['application_id', 'application_date']]
s = s.merge(assess[['application_id', 'dti_ratio']], on='application_id')
s = s[s['application_date'].dt.year.between(2019, 2025)]
result = (100 * (s['dti_ratio'] > 6).groupby(s['application_date'].dt.year.rename('year')).mean()).round(2)
