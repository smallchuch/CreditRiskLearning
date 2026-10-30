# ============================================================================================
# cr02_arrears  |  Q06  |  ★★ core
#
# Share of live loans on a hardship flag at each **quarter-end of 2020** (the COVID deferral
# wave), as a percentage rounded to 2 dp. Return `quarter_end` (`'2020-03-31'` etc.),
# `hardship_pct`; sorted by `quarter_end`.
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

snap = load('loan_monthly_snapshot')

# %% your answer
s = snap[(snap['snapshot_date'].dt.year == 2020) & snap['snapshot_date'].dt.is_quarter_end & (snap['loan_status'] != 'Closed')]
result = (100 * s.groupby(s['snapshot_date'].dt.strftime('%Y-%m-%d').rename('quarter_end'))['hardship_flag'].mean()).round(2)
