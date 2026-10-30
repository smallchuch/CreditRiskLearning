# ============================================================================================
# 12_loops_functions  |  Q08  |  ★★★ challenge
#
# Nested loop to a wide table: approval rate (% of decided applications approved, 2 dp) for
# each `channel` (rows) and application year 2023, 2024, 2025 (columns). Build it with two
# loops into a dict of dicts. Return `channel`, `2023`, `2024`, `2025`; sorted by `channel`.
#
# Return 4 column(s), in the order the question gives them. Expected 4 row(s).
# Sort the output as described.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

app = load('loan_application')

# %% your answer
result = None
