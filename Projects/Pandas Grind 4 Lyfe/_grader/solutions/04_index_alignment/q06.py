# ============================================================================================
# 04_index_alignment  |  Q06  |  ★★ core
#
# Add each loan's `product_name` with `.map` (a Series from `dim_product` used as a lookup),
# then count loans per product name. Return `product_name`, `loans`; sorted by `loans` (most
# first), then `product_name`.
#
# Return 2 column(s), in the order the question gives them. Expected 15 row(s).
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
names = dim_product.set_index('product_id')['product_name']
counts = loan['product_id'].map(names).value_counts().rename_axis('product_name').reset_index(name='loans')
result = counts.sort_values(['loans', 'product_name'], ascending=[False, True])
