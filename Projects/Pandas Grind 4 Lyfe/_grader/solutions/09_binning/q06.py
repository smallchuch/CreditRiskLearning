# ============================================================================================
# 09_binning  |  Q06  |  ★★ core
#
# Band applications by `nsr` (from `assess`) into `'< 1.0'`, `'1.0-1.25'`, `'1.25-1.5'`,
# `'1.5-2.0'`, `'2.0+'` (left-closed), join the decision from `app`, and report the decline
# rate among decided applications. Return `nsr_band`, `apps`, `decline_pct` (2 dp) in band
# order. Leave out empty bands.
#
# Return 3 column(s), in the order the question gives them. Expected 5 row(s).
# Sort the output as described.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

assess = load('application_assessment')
app = load('loan_application')

# %% your answer
m = assess[['application_id', 'nsr']].merge(app[['application_id', 'decision']], on='application_id')
m = m.dropna(subset=['decision'])
labels = ['< 1.0', '1.0-1.25', '1.25-1.5', '1.5-2.0', '2.0+']
m['nsr_band'] = pd.cut(m['nsr'], bins=[-np.inf, 1.0, 1.25, 1.5, 2.0, np.inf], right=False, labels=labels)
result = m.groupby('nsr_band', observed=True).agg(apps=('decision', 'size'),
                                                  decline_pct=('decision', lambda d: round(100 * (d == 'Declined').mean(), 2)))
