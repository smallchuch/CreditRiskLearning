# ============================================================================================
# 05_missing_strings  |  Q03  |  ★ warm-up
#
# The thin-file trap. Return two numbers in one row: the mean `bureau_score` **ignoring**
# thin files, and the mean if thin files were (wrongly) filled with 0. Both rounded to 1 dp;
# columns `mean_skip`, `mean_zero`.
#
# Return 2 column(s), in the order the question gives them. Expected 1 row(s).
# Row order does not matter.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

bureau = load('credit_bureau_report')

# %% your answer
result = None
