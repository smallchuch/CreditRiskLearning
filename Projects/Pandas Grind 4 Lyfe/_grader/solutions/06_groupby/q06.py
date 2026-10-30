# ============================================================================================
# 06_groupby  |  Q06  |  ★★ core
#
# For each loan, compare `original_amount` with the **average for its channel**
# (`transform`). Per channel, how many loans are above their channel average? Return
# `channel`, `above_avg`; sorted by `channel`.
#
# Return 2 column(s), in the order the question gives them. Expected 4 row(s).
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

# %% your answer
avg = loan.groupby('channel')['original_amount'].transform('mean')
result = (loan['original_amount'] > avg).groupby(loan['channel']).sum()
