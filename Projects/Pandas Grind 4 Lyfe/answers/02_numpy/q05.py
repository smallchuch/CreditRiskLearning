# ============================================================================================
# 02_numpy  |  Q05  |  ★★ core
#
# On `bureau`, compare the average `bureau_score` of reports **with** at least one default
# listing (`default_listings > 0`) against those **without**. Thin files (missing score) are
# excluded. Return `group` (`'listed'` / `'clean'`) and `avg_score` rounded to 1 dp; sorted
# by `group`.
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

bureau = load('credit_bureau_report')

# %% your answer
result = None
