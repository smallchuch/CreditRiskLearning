# ============================================================================================
# 05_missing_strings  |  Q04  |  ★★ core
#
# `customer['state']` is written many ways (`'S.A.'`, `'sa'`, `'South Australia'`, `'ACT '`
# ...). Clean it to the eight codes `ACT NSW NT QLD SA TAS VIC WA` and count customers per
# state. Return `state`, `customers`; sorted by `state`.
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

customer = load('customer')

# %% your answer
s = customer['state'].str.strip().str.upper().str.replace('.', '', regex=False)
full = {'SOUTH AUSTRALIA': 'SA', 'VICTORIA': 'VIC', 'NEW SOUTH WALES': 'NSW', 'QUEENSLAND': 'QLD',
        'WESTERN AUSTRALIA': 'WA', 'TASMANIA': 'TAS', 'NORTHERN TERRITORY': 'NT'}
s = s.replace(full)

result = s.value_counts().rename_axis('state').sort_index()
