# ============================================================================================
# 04_index_alignment  |  Q05  |  ★★ core
#
# Put loans per `purpose` for 2024 and 2025 **side by side** with `pd.concat(..., axis=1)`:
# columns `purpose`, `n_2024`, `n_2025`, missing counts as 0. Sorted by `purpose`.
#
# Return 3 column(s), in the order the question gives them. Expected 6 row(s).
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
result = None
