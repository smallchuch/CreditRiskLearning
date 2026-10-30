# ============================================================================================
# 01_python_basics  |  Q05  |  ★★ core
#
# Rank the channels by number of loans (most first) and return a **list of strings** like
# `'1. Broker (35,570)'`.
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
counts = loan['channel'].value_counts()
result = [f"{i}. {name} ({n:,})" for i, (name, n) in enumerate(counts.items(), start=1)]
