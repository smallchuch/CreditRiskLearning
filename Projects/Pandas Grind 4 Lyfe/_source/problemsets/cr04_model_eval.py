from . import P

PRIMER = r"""
**Credit-risk scenario.** Evaluating a score the way notebooks 02 and 03 do: deciles, Gini, KS, capture.
The "model" is the primary applicant's bureau score; the outcome is the loan ever reaching 90+ days past due.

## Building the population (every question starts here)
```python
ever = (snap.groupby('loan_id')['days_past_due'].max() >= 90).astype(int).rename('bad')
prim = applicant[applicant['applicant_role'] == 'Primary'][['application_id', 'customer_id']]
score = prim.merge(bureau[['application_id', 'customer_id', 'bureau_score']], on=['application_id', 'customer_id'])
df = (loan[['loan_id', 'application_id', 'origination_date']].dropna(subset=['application_id'])
        .merge(score[['application_id', 'bureau_score']], on='application_id')
        .merge(ever, left_on='loan_id', right_index=True))
```
Thin files (missing score) are dropped unless the question says otherwise.

## Direction matters
A bureau score is **higher = safer**. `roc_auc_score(actual, predicted_risk)` wants **higher = riskier**, so pass
`-score`. Actuals first, always.

| Metric | Code |
|---|---|
| AUC | `roc_auc_score(df['bad'], -df['bureau_score'])` |
| Gini | `2 * auc - 1` |
| KS | `ks_2samp(score[bad == 1], score[bad == 0]).statistic` (direction doesn't matter) |

## Deciles with ties
Many applicants share a score, so use `rank(method='first')` before `qcut`. Decile 1 = **lowest scores = riskiest**.

## Capture rate
Share of all bads that fall in the worst X% of scores: "the worst 20% of applicants contain 45% of the defaults".
"""

POP = """
ever = (snap.groupby('loan_id')['days_past_due'].max() >= 90).astype(int).rename('bad')
prim = applicant.loc[applicant['applicant_role'] == 'Primary', ['application_id', 'customer_id']]
score = prim.merge(bureau[['application_id', 'customer_id', 'bureau_score']], on=['application_id', 'customer_id'])
df = (loan[['loan_id', 'application_id', 'origination_date']].dropna(subset=['application_id'])
      .merge(score[['application_id', 'bureau_score']], on='application_id')
      .merge(ever, left_on='loan_id', right_index=True))
"""
SCORED = POP + "df = df.dropna(subset=['bureau_score'])\n"
T = ["loan_monthly_snapshot", "application_applicant", "credit_bureau_report", "loan"]

CONCEPT = dict(id="cr04_model_eval", title="cr04 - Score evaluation: deciles, Gini, KS", primer=PRIMER, problems=[
    P(1, """
Build the population (see the primer; thin files dropped). Return one row: `loans`, `bads`, `bad_rate_pct` (3 dp).
""", SCORED + """
result = pd.DataFrame({'loans': [len(df)], 'bads': [int(df['bad'].sum())], 'bad_rate_pct': [round(100 * df['bad'].mean(), 3)]})
""", T, tol=0.0011),

    P(2, """
Score deciles: `rank(method='first')` on `bureau_score`, `qcut` into 10, numbered 1 (lowest scores) to 10.
Return `decile`, `loans`, `bads`, `bad_rate_pct` (2 dp); sorted by `decile`.
""", SCORED + """
df['decile'] = pd.qcut(df['bureau_score'].rank(method='first'), 10, labels=False) + 1
g = df.groupby('decile').agg(loans=('bad', 'size'), bads=('bad', 'sum'))
g['bad_rate_pct'] = (100 * g['bads'] / g['loans']).round(2)
result = g
""", T),

    P(2, """
AUC and Gini of the bureau score (remember the direction). Return one row: `auc`, `gini`, both rounded to 4 dp.
""", SCORED + """
from sklearn.metrics import roc_auc_score
auc = roc_auc_score(df['bad'], -df['bureau_score'])
result = pd.DataFrame({'auc': [round(auc, 4)], 'gini': [round(2 * auc - 1, 4)]})
""", T, tol=0.00011, hint="`roc_auc_score(actuals, risk)`. Higher score = safer, so the risk is `-bureau_score`."),

    P(2, """
KS statistic of the bureau score between bads and goods (`scipy.stats.ks_2samp`), rounded to 4 dp.
""", SCORED + """
from scipy.stats import ks_2samp
s, b = df['bureau_score'].to_numpy(), df['bad'].to_numpy()
result = round(ks_2samp(s[b == 1], s[b == 0]).statistic, 4)
""", T, tol=0.00011),

    P(3, """
Stability: the Gini of the bureau score for each origination year 2019 to 2024, rounded to 4 dp, computed in a loop.
Return `year`, `gini`; sorted by `year`.
""", SCORED + """
from sklearn.metrics import roc_auc_score
yr = df['origination_date'].dt.year
out = {}
for y in range(2019, 2025):
    sub = df[yr == y]
    out[y] = round(2 * roc_auc_score(sub['bad'], -sub['bureau_score']) - 1, 4)
result = pd.Series(out, name='gini').rename_axis('year')
""", T, tol=0.00011),

    P(3, """
Capture rate: what percentage of all bads fall in the **worst 20%** of loans by bureau score (lowest scores; use
`rank(method='first')` so exactly 20% of loans are picked)? Round to 2 dp.
""", SCORED + """
r = df['bureau_score'].rank(method='first')
worst = r <= 0.2 * len(df)
result = round(100 * df.loc[worst, 'bad'].sum() / df['bad'].sum(), 2)
""", T),

    P(2, """
Is a thin file risky? Keep thin files this time. Return `group` (`'scored'` / `'thin file'`), `loans`,
`bad_rate_pct` (3 dp); sorted by `group`.
""", POP + """
df['group'] = np.where(df['bureau_score'].isna(), 'thin file', 'scored')
result = df.groupby('group').agg(loans=('bad', 'size'), bad_rate_pct=('bad', 'mean'))
result['bad_rate_pct'] = (100 * result['bad_rate_pct']).round(3)
""", T, tol=0.0011),
])
