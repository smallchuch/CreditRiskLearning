# ============================================================================================
# 07_merge  |  Q08  |  ★★★ challenge
#
# Arrears bucket for each live loan at 2025-12-31 using `ref_arrears_bucket` (`merge_asof`
# on `days_past_due` against `dpd_from`). Return `bucket_name`, `loans` for every bucket
# that has loans; sorted by `bucket_id` (so in bucket order, not alphabetical).
#
# Return 2 column(s), in the order the question gives them. Expected 7 row(s).
# Sort the output as described.
# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).
# ============================================================================================

# %% setup (runs every time - each file must stand on its own)
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))
import numpy as np
import pandas as pd
from grind import load

snap = load('loan_monthly_snapshot')
ref_arrears_bucket = load('ref_arrears_bucket')

# %% your answer
live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')]
l = live[['loan_id', 'days_past_due']].sort_values('days_past_due')
b = ref_arrears_bucket.sort_values('dpd_from')
m = pd.merge_asof(l, b, left_on='days_past_due', right_on='dpd_from')
result = (m.groupby(['bucket_id', 'bucket_name']).size().rename('loans').reset_index()
          .sort_values('bucket_id')[['bucket_name', 'loans']])
