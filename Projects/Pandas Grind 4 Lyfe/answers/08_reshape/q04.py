# ============================================================================================
# 08_reshape  |  Q04  |  ★★ core
#
# Melt `dim_product[['product_id', 'max_lvr_pct', 'annual_fee']]` into long form. Return
# `product_id`, `variable`, `value`; sorted by `product_id`, then `variable`.
#
# Return 3 column(s), in the order the question gives them. Expected 30 row(s).
# Sort the output as described.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

dim_product = load('dim_product')

# %% your answer
result = None
