# ============================================================================================
# cr05_origination  |  Q02  |  ★ warm-up
#
# Decline reasons: share of declined applications by `reason_description` (join
# `ref_decline_reason`), % to 2 dp. Return `reason_description`, `pct`; sorted by `pct`
# (largest first).
#
# Return 2 column(s), in the order the question gives them. Expected 8 row(s).
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
result = (100 * d['reason_description'].value_counts(normalize=True)).round(2).sort_values(ascending=False)
