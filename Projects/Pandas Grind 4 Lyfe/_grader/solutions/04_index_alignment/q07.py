# ============================================================================================
# 04_index_alignment  |  Q07  |  ★★★ challenge
#
# Count loans by `rate_type` and `channel` (a two-level index), then select just the
# `'Fixed'` part with `.loc`. Return `channel`, `loans`; sorted by `channel`.
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

loan = load('loan')

# %% your answer
s = loan.groupby(['rate_type', 'channel']).size()
result = s.loc['Fixed'].sort_index()
