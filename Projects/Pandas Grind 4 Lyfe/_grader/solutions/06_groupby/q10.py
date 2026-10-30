# ============================================================================================
# 06_groupby  |  Q10  |  ★★★ challenge
#
# On `app`, among applications that have a `decision`, the approval rate per `channel` as a
# percentage rounded to 2 dp. Return `channel`, `approval_pct`; sorted by `channel`.
#
# Return 2 column(s), in the order the question gives them. Expected 4 row(s).
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
d = app.dropna(subset=['decision'])
result = (100 * (d['decision'] == 'Approved').groupby(d['channel']).mean()).round(2)
