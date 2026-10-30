# ============================================================================================
# 07_merge  |  Q06  |  ★★ core
#
# The **primary** applicant's bureau score per application: join `applicant` (role
# `'Primary'`) to `bureau` on **both** `application_id` and `customer_id`, then join `app`
# for the decision. Average `bureau_score` (thin files excluded) per `decision`, rounded to
# 1 dp. Return `decision`, `avg_score`; sorted by `decision`.
#
# Return 2 column(s), in the order the question gives them. Expected 2 row(s).
# Sort the output as described.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

applicant = load('application_applicant')
bureau = load('credit_bureau_report')
app = load('loan_application')

# %% your answer
result = None
