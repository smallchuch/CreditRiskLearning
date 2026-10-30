# ============================================================================================
# 07_merge  |  Q05  |  ★★ core
#
# Loans per **branch state** (join `dim_branch` on `branch_id` with
# `validate='many_to_one'`; loans with no branch are left out). Return `state`, `loans`;
# sorted by `loans` (most first), then `state`.
#
# Return 2 column(s), in the order the question gives them. Expected 8 row(s).
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
dim_branch = load('dim_branch')

# %% your answer
result = None
