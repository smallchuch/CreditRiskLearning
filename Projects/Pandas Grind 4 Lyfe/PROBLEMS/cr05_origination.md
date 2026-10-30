# cr05 - Origination and serviceability

`answers/cr05_origination/qNN.py` &nbsp;|&nbsp; check with: `grade cr05` or `grade cr05 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

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

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Decline rate (% of decided applications that were declined, 2 dp) by **application month** of 2025, month as `'2025-01'`.
Return `month`, `decline_pct`; sorted by `month`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `app`

### Q02 &nbsp; ★ &nbsp; (warm-up)

Decline reasons: share of declined applications by `reason_description` (join `ref_decline_reason`), % to 2 dp.
Return `reason_description`, `pct`; sorted by `pct` (largest first).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `app`, `ref_decline_reason`

### Q03 &nbsp; ★★ &nbsp; (core)

Declines by **reason category** (the credit 'C': Capacity, Character, ...) and application year 2023 to 2025, as counts.
Return `reason_category`, `2023`, `2024`, `2025`; sorted by `reason_category`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `app`, `ref_decline_reason`

### Q04 &nbsp; ★★ &nbsp; (core)

How often does HEM bind? Percentage of applications with `hem_applied_flag` True, by application year 2019 to 2025
(2 dp). Return `year`, `hem_pct`; sorted by `year`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `app`, `assess`

### Q05 &nbsp; ★★ &nbsp; (core)

Recompute the surplus: `assessed_net_monthly_income - assessed_living_expenses - assessed_commitments_monthly
- new_loan_assessed_repayment`. How many applications differ from the stored `monthly_surplus` by more than $1?

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `assess`

### Q06 &nbsp; ★★ &nbsp; (core)

Settled loans with a DTI above 6 (`assess.dti_ratio > 6`), as a % of settled applications per application year 2019
to 2025 (2 dp). Return `year`, `dti6_pct`; sorted by `year`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `app`, `assess`

### Q07 &nbsp; ★★★ &nbsp; (challenge)

Policy in force: attach the `ref_serviceability_policy` row in force at each application's `application_date`
(`merge_asof` on `effective_from`). For **approved** applications, how many have `nsr` below that policy's `min_nsr`
(policy exceptions, by the numbers)? Return `policy_id`, `approved`, `below_min_nsr`; sorted by `policy_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `app`, `assess`, `ref_serviceability_policy`
