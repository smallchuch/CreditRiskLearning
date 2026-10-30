from . import P

PRIMER = r"""
**Credit-risk scenario.** Vintage analysis: the warm-up for Freddie Mac stage 02. Patterns from sets 08, 10, 11.

## A vintage curve is a pivot

```
 one row per loan-month (snap)            ->   vintage x MOB table
 loan  vintage  mob  dpd  ever90_so_far          MOB:   6     12     18     24
 A     2021     0    0    0                      2019  0.4%  1.1%  1.8%  2.2%
 A     2021     1    0    0                      2020  0.3%  0.9%  1.6%  2.1%
 ...                                             2021  ...
```

## The recipe (cumulative ever-90 by MOB)
1. Vintage of each loan = origination year (or quarter: `dt.to_period('Q')`).
2. For each loan, the **first MOB** at which it reached 90+ (NaN if never).
3. For each vintage and target MOB m: share of the vintage's loans whose first-90+ MOB is `<= m`.
4. **Denominator = every loan in the vintage**, including ones that closed early (they can't go bad later; that's the
   usual "cumulative bad rate" convention).

## Censoring
A 2025 vintage can't have a MOB-24 value yet. Only include vintages old enough for the MOB you're reporting
(the questions say which).

## Point-in-time vs cumulative
- **Cumulative** ever-90 by MOB 12: went bad at any point up to MOB 12. Only goes up with MOB.
- **Point-in-time** 30+ at MOB 12: in arrears *at* MOB 12, among loans still on book then. Can go down (cures).
"""

FIRST90 = """
first90 = snap[snap['days_past_due'] >= 90].groupby('loan_id')['months_on_book'].min().rename('first90_mob')
v = loan[['loan_id', 'origination_date', 'original_amount']].merge(first90, left_on='loan_id', right_index=True, how='left')
v['vintage'] = v['origination_date'].dt.year
"""

CONCEPT = dict(id="cr03_vintage", title="cr03 - Vintage analysis", primer=PRIMER, problems=[
    P(1, """
Loans per **origination quarter** for 2023 vintages, as strings like `'2023Q1'`. Return `vintage`, `loans`; sorted by `vintage`.
""", """
l = loan[loan['origination_date'].dt.year == 2023]
result = l['origination_date'].dt.to_period('Q').astype(str).value_counts().sort_index().rename_axis('vintage')
""", ["loan"]),

    P(2, """
Cumulative ever-90 rate **by MOB 12** for vintages 2019 to 2024: the percentage of each vintage's loans whose first
90+ month-end came at `months_on_book <= 12`. Denominator = all loans in the vintage. Return `vintage`, `pct` (2 dp);
sorted by `vintage`.
""", FIRST90 + """
v = v[v['vintage'].between(2019, 2024)]
result = (100 * (v['first90_mob'] <= 12).groupby(v['vintage']).mean()).round(2)
""", ["loan_monthly_snapshot", "loan"]),

    P(3, """
The full vintage table: rows = vintages 2019 to 2023, columns = MOB 6, 12, 18, 24, values = cumulative ever-90 % by
that MOB (2 dp). Return `vintage`, `6`, `12`, `18`, `24`; sorted by `vintage`.
""", FIRST90 + """
v = v[v['vintage'].between(2019, 2023)]
cols = {}
for m in [6, 12, 18, 24]:
    cols[m] = (100 * (v['first90_mob'] <= m).groupby(v['vintage']).mean()).round(2)
result = pd.DataFrame(cols).rename_axis('vintage')
""", ["loan_monthly_snapshot", "loan"], hint="One column per MOB is a natural loop: `for m in [6, 12, 18, 24]`."),

    P(2, """
**Point-in-time** 30+ rate at MOB 12 by vintage 2019 to 2024: among loans that have a snapshot at `months_on_book == 12`
(and are not `'Closed'` in it), the percentage with `days_past_due >= 30` in that snapshot. Return `vintage`, `pct` (2 dp);
sorted by `vintage`.
""", """
s = snap[(snap['months_on_book'] == 12) & (snap['loan_status'] != 'Closed')]
s = s.merge(loan[['loan_id', 'origination_date']], on='loan_id')
s['vintage'] = s['origination_date'].dt.year
s = s[s['vintage'].between(2019, 2024)]
result = (100 * (s['days_past_due'] >= 30).groupby(s['vintage']).mean()).round(2)
""", ["loan_monthly_snapshot", "loan"]),

    P(3, """
**Balance-weighted** cumulative ever-90 by MOB 24 for vintages 2019 to 2023: original amount of loans that went 90+ by
MOB 24 / original amount of the whole vintage, as % (2 dp). Return `vintage`, `pct_by_amount`; sorted by `vintage`.
""", FIRST90 + """
v = v[v['vintage'].between(2019, 2023)].copy()
v['bad_amt'] = v['original_amount'].where(v['first90_mob'] <= 24, 0)
g = v.groupby('vintage')[['bad_amt', 'original_amount']].sum()
result = (100 * g['bad_amt'] / g['original_amount']).round(2)
""", ["loan_monthly_snapshot", "loan"]),

    P(3, """
Survival: for vintages 2019 to 2023, the percentage of each vintage's loans that still had a non-`'Closed'` snapshot at
MOB 24. Return `vintage`, `pct_open_mob24` (2 dp); sorted by `vintage`.
""", """
open24 = set(snap.loc[(snap['months_on_book'] == 24) & (snap['loan_status'] != 'Closed'), 'loan_id'])
v = loan[loan['origination_date'].dt.year.between(2019, 2023)]
result = (100 * v['loan_id'].isin(open24).groupby(v['origination_date'].dt.year.rename('vintage')).mean()).round(2)
""", ["loan_monthly_snapshot", "loan"]),
])
