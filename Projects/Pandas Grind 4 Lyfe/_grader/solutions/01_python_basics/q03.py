# ============================================================================================
# 01_python_basics  |  Q03  |  ★ warm-up
#
# A **dict** mapping `product_id` to `product_name` for every product. Return the dict (it
# is graded as key, value pairs).
#
# Return 2 column(s), in the order the question gives them. Expected 15 row(s).
# Row order does not matter.
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
result = dict(zip(dim_product['product_id'], dim_product['product_name']))
