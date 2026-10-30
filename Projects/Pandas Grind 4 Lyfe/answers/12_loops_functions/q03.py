# ============================================================================================
# 12_loops_functions  |  Q03  |  ★★ core
#
# Build a **list of dicts** in a loop over origination years 2019 to 2025 (one dict per
# year), then make a DataFrame. Each row: `year`, `loans`, `avg_lvr` (2 dp), `pct_fixed` (2
# dp). Sorted by `year`.
#
# Return 4 column(s), in the order the question gives them. Expected 7 row(s).
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
result = None
