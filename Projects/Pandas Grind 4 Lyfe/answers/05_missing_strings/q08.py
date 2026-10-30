# ============================================================================================
# 05_missing_strings  |  Q08  |  ★★ core
#
# Mobile numbers come in mixed formats (`'0412345678'`, `'+61 412 345 678'`, `'0412 345
# 678'` ...). Normalise each to 10 digits starting `04` (remove spaces, turn a leading `+61`
# into `0`). How many customers' numbers were **not** already in that clean form?
#
# Return 1 column(s), in the order the question gives them. Expected 1 row(s).
# Row order does not matter.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

customer = load('customer')

# %% your answer
result = None
