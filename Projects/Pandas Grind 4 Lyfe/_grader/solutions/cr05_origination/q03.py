# ============================================================================================
# cr05_origination  |  Q03  |  ★★ core
#
# Declines by **reason category** (the credit 'C': Capacity, Character, ...) and application
# year 2023 to 2025, as counts. Return `reason_category`, `2023`, `2024`, `2025`; sorted by
# `reason_category`.
#
# Return 4 column(s), in the order the question gives them. Expected 6 row(s).
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
ref_decline_reason = load('ref_decline_reason')

# %% your answer
d = app[app['decision'] == 'Declined'].merge(ref_decline_reason, left_on='decline_reason_code', right_on='reason_code')
d = d[d['application_date'].dt.year.between(2023, 2025)]
result = pd.crosstab(d['reason_category'], d['application_date'].dt.year)
