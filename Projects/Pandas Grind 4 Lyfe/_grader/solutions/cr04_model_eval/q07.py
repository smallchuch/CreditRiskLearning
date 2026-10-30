# ============================================================================================
# cr04_model_eval  |  Q07  |  ★★ core
#
# Is a thin file risky? Keep thin files this time. Return `group` (`'scored'` / `'thin
# file'`), `loans`, `bad_rate_pct` (3 dp); sorted by `group`.
#
# Return 3 column(s), in the order the question gives them. Expected 2 row(s).
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

df['group'] = np.where(df['bureau_score'].isna(), 'thin file', 'scored')
result = df.groupby('group').agg(loans=('bad', 'size'), bad_rate_pct=('bad', 'mean'))
result['bad_rate_pct'] = (100 * result['bad_rate_pct']).round(3)
