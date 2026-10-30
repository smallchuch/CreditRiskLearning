# ============================================================================================
# 10_dates  |  Q06  |  ★★ core
#
# New hardship arrangements per month in **2020** (`start_date`), every month of 2020
# present (0 if none), month as a string like `'2020-04'`. Return `month`, `arrangements`;
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

hardship_arrangement = load('hardship_arrangement')

# %% your answer
result = None
