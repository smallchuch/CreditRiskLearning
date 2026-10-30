# cr04 - Score evaluation: deciles, Gini, KS

`answers/cr04_model_eval/qNN.py` &nbsp;|&nbsp; check with: `grade cr04` or `grade cr04 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

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

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Build the population (see the primer; thin files dropped). Return one row: `loans`, `bads`, `bad_rate_pct` (3 dp).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`, `applicant`, `bureau`, `loan`

### Q02 &nbsp; ★★ &nbsp; (core)

Score deciles: `rank(method='first')` on `bureau_score`, `qcut` into 10, numbered 1 (lowest scores) to 10.
Return `decile`, `loans`, `bads`, `bad_rate_pct` (2 dp); sorted by `decile`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `applicant`, `bureau`, `loan`

### Q03 &nbsp; ★★ &nbsp; (core)

AUC and Gini of the bureau score (remember the direction). Return one row: `auc`, `gini`, both rounded to 4 dp.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`, `applicant`, `bureau`, `loan`

<details><summary>hint</summary>

`roc_auc_score(actuals, risk)`. Higher score = safer, so the risk is `-bureau_score`.

</details>

### Q04 &nbsp; ★★ &nbsp; (core)

KS statistic of the bureau score between bads and goods (`scipy.stats.ks_2samp`), rounded to 4 dp.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`, `applicant`, `bureau`, `loan`

### Q05 &nbsp; ★★★ &nbsp; (challenge)

Stability: the Gini of the bureau score for each origination year 2019 to 2024, rounded to 4 dp, computed in a loop.
Return `year`, `gini`; sorted by `year`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `applicant`, `bureau`, `loan`

### Q06 &nbsp; ★★★ &nbsp; (challenge)

Capture rate: what percentage of all bads fall in the **worst 20%** of loans by bureau score (lowest scores; use
`rank(method='first')` so exactly 20% of loans are picked)? Round to 2 dp.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`, `applicant`, `bureau`, `loan`

### Q07 &nbsp; ★★ &nbsp; (core)

Is a thin file risky? Keep thin files this time. Return `group` (`'scored'` / `'thin file'`), `loans`,
`bad_rate_pct` (3 dp); sorted by `group`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `applicant`, `bureau`, `loan`
