# ============================================================================================
# 08_reshape  |  Q07  |  ★★ core
#
# `ref_property_price_index` for 2025 month-ends: `pivot` so each row is a `month_end_date`
# and the columns are `NSW` and `SA` (just those two states). Return `month_end_date`,
# `NSW`, `SA`; sorted by `month_end_date`.
#
# Return 3 column(s), in the order the question gives them. Expected 12 row(s).
# Sort the output as described.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

ref_property_price_index = load('ref_property_price_index')

# %% your answer
result = None
