# ============================================================================================
# 01_python_basics  |  Q02  |  ★ warm-up
#
# The distinct `channel` values on `loan`, in alphabetical order, as a plain Python
# **list**.
#
# Return 1 column(s), in the order the question gives them. Expected 4 row(s).
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
result = sorted(loan['channel'].unique())
