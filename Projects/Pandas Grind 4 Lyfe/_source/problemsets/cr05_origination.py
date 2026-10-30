from . import P

PRIMER = r"""
**Credit-risk scenario.** Origination and serviceability: your day job, in pandas. Patterns from sets 06, 07, 09, 10.

## The application tables

```
 app (loan_application)        one row per application: channel, purpose, decision, decline_reason_code ...
 assess (application_assessment) one row per application: nsr, dti_ratio, lvr_pct, hem_applied_flag, buffer ...
 ref_decline_reason            reason_code -> description, category (Capacity, Character, Collateral ...)
 ref_serviceability_policy     policy epochs: buffer, floor, min NSR, max LVR, max DTI
```
Join on `application_id`. "Decided" = `decision` not missing.

## Serviceability, as stored in `assess`
```
 monthly_surplus = assessed_net_monthly_income
                 - assessed_living_expenses        (the higher of declared and HEM)
                 - assessed_commitments_monthly
                 - new_loan_assessed_repayment     (at product rate + buffer, or the floor)
 nsr             = assessed_net_monthly_income
                 / (living expenses + commitments + new repayment)   (net surplus ratio: 1.0 = break-even)
```

## Policy epochs: a range join
`ref_serviceability_policy` has `effective_from` / `effective_to`. To find the policy in force at an application date,
`merge_asof` on the date (sorted), the same trick as the RBA cash rate in set 07.
"""

CONCEPT = dict(id="cr05_origination", title="cr05 - Origination and serviceability", primer=PRIMER, problems=[
    P(1, """
Decline rate (% of decided applications that were declined, 2 dp) by **application month** of 2025, month as `'2025-01'`.
Return `month`, `decline_pct`; sorted by `month`.
""", """
d = app[(app['application_date'].dt.year == 2025) & app['decision'].notna()]
result = (100 * (d['decision'] == 'Declined').groupby(d['application_date'].dt.strftime('%Y-%m').rename('month')).mean()).round(2)
""", ["loan_application"]),

    P(1, """
Decline reasons: share of declined applications by `reason_description` (join `ref_decline_reason`), % to 2 dp.
Return `reason_description`, `pct`; sorted by `pct` (largest first).
""", """
d = app[app['decision'] == 'Declined'].merge(ref_decline_reason, left_on='decline_reason_code', right_on='reason_code')
result = (100 * d['reason_description'].value_counts(normalize=True)).round(2).sort_values(ascending=False)
""", ["loan_application", "ref_decline_reason"]),

    P(2, """
Declines by **reason category** (the credit 'C': Capacity, Character, ...) and application year 2023 to 2025, as counts.
Return `reason_category`, `2023`, `2024`, `2025`; sorted by `reason_category`.
""", """
d = app[app['decision'] == 'Declined'].merge(ref_decline_reason, left_on='decline_reason_code', right_on='reason_code')
d = d[d['application_date'].dt.year.between(2023, 2025)]
result = pd.crosstab(d['reason_category'], d['application_date'].dt.year)
""", ["loan_application", "ref_decline_reason"]),

    P(2, """
How often does HEM bind? Percentage of applications with `hem_applied_flag` True, by application year 2019 to 2025
(2 dp). Return `year`, `hem_pct`; sorted by `year`.
""", """
m = app[['application_id', 'application_date']].merge(assess[['application_id', 'hem_applied_flag']], on='application_id')
m = m[m['application_date'].dt.year.between(2019, 2025)]
result = (100 * m.groupby(m['application_date'].dt.year.rename('year'))['hem_applied_flag'].mean()).round(2)
""", ["loan_application", "application_assessment"]),

    P(2, """
Recompute the surplus: `assessed_net_monthly_income - assessed_living_expenses - assessed_commitments_monthly
- new_loan_assessed_repayment`. How many applications differ from the stored `monthly_surplus` by more than $1?
""", """
calc = (assess['assessed_net_monthly_income'] - assess['assessed_living_expenses']
        - assess['assessed_commitments_monthly'] - assess['new_loan_assessed_repayment'])
result = int(((calc - assess['monthly_surplus']).abs() > 1).sum())
""", ["application_assessment"], empty_ok=True),

    P(2, """
Settled loans with a DTI above 6 (`assess.dti_ratio > 6`), as a % of settled applications per application year 2019
to 2025 (2 dp). Return `year`, `dti6_pct`; sorted by `year`.
""", """
s = app.loc[app['current_status'] == 'Settled', ['application_id', 'application_date']]
s = s.merge(assess[['application_id', 'dti_ratio']], on='application_id')
s = s[s['application_date'].dt.year.between(2019, 2025)]
result = (100 * (s['dti_ratio'] > 6).groupby(s['application_date'].dt.year.rename('year')).mean()).round(2)
""", ["loan_application", "application_assessment"]),

    P(3, """
Policy in force: attach the `ref_serviceability_policy` row in force at each application's `application_date`
(`merge_asof` on `effective_from`). For **approved** applications, how many have `nsr` below that policy's `min_nsr`
(policy exceptions, by the numbers)? Return `policy_id`, `approved`, `below_min_nsr`; sorted by `policy_id`.
""", """
a = app.loc[app['decision'] == 'Approved', ['application_id', 'application_date']].sort_values('application_date')
pol = ref_serviceability_policy[['policy_id', 'effective_from', 'min_nsr']].sort_values('effective_from')
m = pd.merge_asof(a, pol, left_on='application_date', right_on='effective_from')
m = m.merge(assess[['application_id', 'nsr']], on='application_id')
m['below'] = m['nsr'] < m['min_nsr']
result = m.groupby('policy_id').agg(approved=('below', 'size'), below_min_nsr=('below', 'sum'))
""", ["loan_application", "application_assessment", "ref_serviceability_policy"]),
])
