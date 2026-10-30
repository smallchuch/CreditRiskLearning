# ============================================================================================
# cr04_model_eval  |  Q05  |  ★★★ challenge
#
# Stability: the Gini of the bureau score for each origination year 2019 to 2024, rounded to
# 4 dp, computed in a loop. Return `year`, `gini`; sorted by `year`.
#
# Return 2 column(s), in the order the question gives them. Expected 6 row(s).
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
applicant = load('application_applicant')
bureau = load('credit_bureau_report')
loan = load('loan')

# %% your answer
ever = (snap.groupby('loan_id')['days_past_due'].max() >= 90).astype(int).rename('bad')
prim = applicant.loc[applicant['applicant_role'] == 'Primary', ['application_id', 'customer_id']]
score = prim.merge(bureau[['application_id', 'customer_id', 'bureau_score']], on=['application_id', 'customer_id'])
df = (loan[['loan_id', 'application_id', 'origination_date']].dropna(subset=['application_id'])
      .merge(score[['application_id', 'bureau_score']], on='application_id')
      .merge(ever, left_on='loan_id', right_index=True))
df = df.dropna(subset=['bureau_score'])

from sklearn.metrics import roc_auc_score
yr = df['origination_date'].dt.year
out = {}
for y in range(2019, 2025):
    sub = df[yr == y]
    out[y] = round(2 * roc_auc_score(sub['bad'], -sub['bureau_score']) - 1, 4)
result = pd.Series(out, name='gini').rename_axis('year')
