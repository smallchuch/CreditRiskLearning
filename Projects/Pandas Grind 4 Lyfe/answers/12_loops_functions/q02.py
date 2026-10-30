# ============================================================================================
# 12_loops_functions  |  Q02  |  ★★ core
#
# Segments as a dict of masks:
#
# ```python
# segments = {
#     'All':        all loans,
#     'FHB':        first_home_buyer_flag is True,
#     'Fixed':      rate_type == 'Fixed',
#     'High LVR':   lvr_at_origination_pct > 80,
# }
# ```
#
# For each, `loans` and `avg_amount` (mean `original_amount`, 0 dp). Return `segment`,
# `loans`, `avg_amount`; sorted by `segment`.
#
# Return 3 column(s), in the order the question gives them. Expected 4 row(s).
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
