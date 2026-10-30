# ============================================================================================
# cr02_arrears  |  Q04  |  ★★★ challenge
#
# Roll-rate matrix November -> December 2025 for loans that are live (not `'Closed'`) in
# **both** month-end snapshots. Buckets `Current`, `1-29`, `30-59`, `60-89`, `90+`; **row
# percentages** rounded to 2 dp, 0 where nothing rolled. Return `from_bucket` then one
# column per December bucket in bucket order; rows in bucket order.
#
# Return 6 column(s), in the order the question gives them. Expected 5 row(s).
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

# %% your answer
order = ['Current', '1-29', '30-59', '60-89', '90+']
def bucket(dpd):
    return pd.Categorical(pd.cut(dpd, [-1, 0, 29, 59, 89, np.inf], labels=order), categories=order, ordered=True)

open_ = snap['loan_status'] != 'Closed'
nov = snap.loc[(snap['snapshot_date'] == '2025-11-30') & open_, ['loan_id', 'days_past_due']]
dec = snap.loc[(snap['snapshot_date'] == '2025-12-31') & open_, ['loan_id', 'days_past_due']]
m = nov.merge(dec, on='loan_id', suffixes=('_nov', '_dec'))
t = pd.crosstab(bucket(m['days_past_due_nov']), bucket(m['days_past_due_dec']), normalize='index', dropna=False)
t = t.reindex(index=order, columns=order, fill_value=0)
result = (100 * t).round(2).rename_axis('from_bucket')
