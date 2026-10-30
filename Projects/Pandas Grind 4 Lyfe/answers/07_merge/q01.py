# ============================================================================================
# 07_merge  |  Q01  |  ★ warm-up
#
# Bring `occupancy` from `dim_product` onto `loan` and count loans per occupancy. Return
# `occupancy`, `loans`; sorted by `occupancy`.
#
# Return 2 column(s), in the order the question gives them. Expected 2 row(s).
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
dim_product = load('dim_product')

# %% your answer
result = None
