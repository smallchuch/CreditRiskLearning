# ============================================================================================
# 05_missing_strings  |  Q07  |  ★★ core
#
# Duplicate customers: the same person (first name, last name and date of birth, ignoring
# case and spaces) under more than one `customer_id`. Customers with no date of birth are
# left out. How many **extra** records are there (rows minus distinct people)?
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
