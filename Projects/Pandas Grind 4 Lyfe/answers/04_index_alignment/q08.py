# ============================================================================================
# 04_index_alignment  |  Q08  |  ★★★ challenge
#
# New loans per calendar month of **2023** for the `'Construction'` purpose. Every month 1
# to 12 must appear, with 0 where there were none (`reindex`). Return `month`, `loans`;
# sorted by `month`.
#
# Return 2 column(s), in the order the question gives them. Expected 12 row(s).
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
