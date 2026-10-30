# ============================================================================================
# 04_index_alignment  |  Q02  |  ★ warm-up
#
# Loans per channel as a DataFrame with **columns** `channel`, `loans` (not an index).
# Sorted by `channel`.
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
result = loan['channel'].value_counts().rename_axis('channel').reset_index(name='loans').sort_values('channel')
