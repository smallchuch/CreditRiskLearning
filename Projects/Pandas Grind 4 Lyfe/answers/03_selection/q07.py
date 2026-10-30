# ============================================================================================
# 03_selection  |  Q07  |  ★★ core
#
# Products whose `product_name` contains the word `'Fixed'`. Return `product_id`,
# `product_name`, `fixed_term_months`; sorted by `product_id`.
#
# Return 3 column(s), in the order the question gives them. Expected 5 row(s).
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
