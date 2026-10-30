# ============================================================================================
# cr05_origination  |  Q04  |  ★★ core
#
# How often does HEM bind? Percentage of applications with `hem_applied_flag` True, by
# application year 2019 to 2025 (2 dp). Return `year`, `hem_pct`; sorted by `year`.
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
m = app[['application_id', 'application_date']].merge(assess[['application_id', 'hem_applied_flag']], on='application_id')
m = m[m['application_date'].dt.year.between(2019, 2025)]
result = (100 * m.groupby(m['application_date'].dt.year.rename('year'))['hem_applied_flag'].mean()).round(2)
