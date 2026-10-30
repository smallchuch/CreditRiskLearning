# ============================================================================================
# 07_merge  |  Q03  |  ★★ core
#
# Anti-join: how many customers are **never** the `primary_customer_id` on a loan?
# (`indicator=True`)
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
loan = load('loan')

# %% your answer
m = customer[['customer_id']].merge(loan[['primary_customer_id']].drop_duplicates(),
                                    left_on='customer_id', right_on='primary_customer_id',
                                    how='left', indicator=True)
result = int((m['_merge'] == 'left_only').sum())
