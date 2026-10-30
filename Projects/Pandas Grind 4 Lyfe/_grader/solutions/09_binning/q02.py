# ============================================================================================
# 09_binning  |  Q02  |  ★ warm-up
#
# Deciles of `original_amount` with `pd.qcut(q=10, labels=False)`, numbered **1 to 10**.
# Return `decile`, `min_amount`, `max_amount`; sorted by `decile`.
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

loan = load('loan')

# %% your answer
d = pd.qcut(loan['original_amount'], q=10, labels=False, duplicates='drop') + 1
result = loan.groupby(d.rename('decile'))['original_amount'].agg(['min', 'max'])
