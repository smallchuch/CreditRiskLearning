# ============================================================================================
# 09_binning  |  Q03  |  ★★ core
#
# Bureau-score deciles that never fail on ties: rank the non-missing `bureau_score` values
# with `method='first'`, then `qcut` the rank into 10 groups numbered 1 (lowest scores) to
# 10. Return `decile`, `n`, `avg_score` (1 dp); sorted by `decile`.
#
# Return 3 column(s), in the order the question gives them. Expected 10 row(s).
# Sort the output as described.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

bureau = load('credit_bureau_report')

# %% your answer
s = bureau['bureau_score'].dropna()
d = pd.qcut(s.rank(method='first'), q=10, labels=False) + 1
result = s.groupby(d.rename('decile')).agg(n='size', avg_score='mean')
result['avg_score'] = result['avg_score'].round(1)
