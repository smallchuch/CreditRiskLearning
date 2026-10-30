# ============================================================================================
# cr04_model_eval  |  Q04  |  ★★ core
#
# KS statistic of the bureau score between bads and goods (`scipy.stats.ks_2samp`), rounded
# to 4 dp.
#
# Return 1 column(s), in the order the question gives them. Expected 1 row(s).
# Row order does not matter.
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

from scipy.stats import ks_2samp
s, b = df['bureau_score'].to_numpy(), df['bad'].to_numpy()
result = round(ks_2samp(s[b == 1], s[b == 0]).statistic, 4)
