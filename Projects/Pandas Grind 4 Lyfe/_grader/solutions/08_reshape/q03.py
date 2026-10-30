# ============================================================================================
# 08_reshape  |  Q03  |  ★★ core
#
# Group by origination year and `channel`, count, then `unstack` the channel (missing = 0).
# Return `year`, then one column per channel in alphabetical order (`Branch`, `Broker`,
# `Digital`, `Mobile Lender`); sorted by `year`.
#
# Return 5 column(s), in the order the question gives them. Expected 8 row(s).
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
result = loan.groupby([loan['origination_date'].dt.year.rename('year'), 'channel']).size().unstack(fill_value=0)
