# ============================================================================================
# cr05_origination  |  Q07  |  ★★★ challenge
#
# Policy in force: attach the `ref_serviceability_policy` row in force at each application's
# `application_date` (`merge_asof` on `effective_from`). For **approved** applications, how
# many have `nsr` below that policy's `min_nsr` (policy exceptions, by the numbers)? Return
# `policy_id`, `approved`, `below_min_nsr`; sorted by `policy_id`.
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

app = load('loan_application')
assess = load('application_assessment')
ref_serviceability_policy = load('ref_serviceability_policy')

# %% your answer
result = None
