# ============================================================================================
# 01_python_basics  |  Q01  |  ★ warm-up
#
# Total original lending across all loans, as a **string** formatted like `$12,345,678`
# (dollar sign, thousands commas, no decimals). Return the string.
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

loan = load('loan')

# %% your answer
result = None
# %%
loan.describe()
# %%
