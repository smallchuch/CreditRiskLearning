# CR08 - Hardship and collections

`answers/cr08_hardship_collections/qNN.sql` &nbsp;|&nbsp; check with: `grade cr08` or `grade cr08 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Scenario: the customers who are struggling

Collections and Hardship teams work the arrears queue. Analytics answers: *what are we doing, and does it work?*

```
 arrears -> hardship invitation letter -> call -> promise to pay -> kept? -> cured / escalated -> default notice -> legal -> possession
```
Tables:
* `hardship_arrangement` - temporary relief (deferrals, reduced repayments, term extension, capitalisation). `arrangement_outcome`: Returned to normal repayments / Moved into arrears / Loan closed during arrangement.
* `collections_activity` - every contact attempt (`activity_type`, `outcome`, `days_past_due_at_activity`, promises and whether kept).
* `loan_event` - 'Hardship arrangement started', 'Entered recovery - possession process'.
* COVID deferrals (`'COVID-19 repayment deferral'`) are a distinct 2020-21 wave - analysts always split them from "normal" hardship.

Metrics: **promise-kept rate**, **cure after hardship**, **contacts per account**, **time from first arrears to first contact**.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Hardship arrangements by type and status: `hardship_type`, `arrangements`, `still_active` (status Active); sorted by arrangements descending then type.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Hardship arrangements started per year. `yr`, `arrangements`; sorted by year.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Collections activity volume by `activity_type`. `activity_type`, `n`; sorted by n descending then type.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **11 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

Non-COVID hardship outcomes: for arrangements that are `Completed` and not COVID-19 deferrals, the % with each outcome. `arrangement_outcome`, `n`, `pct` (1dp); sorted by n descending then outcome.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

Promise-to-pay performance: of promises (`promise_amount` not null), the % kept (`promise_kept_flag`) by `activity_type` (1dp). `activity_type`, `promises`, `kept_pct`; sorted by activity type.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

Average planned arrangement length in months (1dp) by hardship type for non-COVID types. `hardship_type`, `avg_planned_months`; sorted by type.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

Collections contacts per loan: distribution of the number of activity rows per loan: `contacts_bucket` (`1-3`, `4-10`, `11+`), `loans`; sorted by bucket's lower bound.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

Dishonoured payments: `loan_payment` rows with `payment_status = 'Dishonoured'` by `failure_reason`. `failure_reason`, `n`; sorted by n descending then reason.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★★ &nbsp; (challenge)

First contact lag: for each loan, days from the first snapshot where dpd >= 30 to its first `collections_activity` on or after that date. Median lag (days) across loans that have both. One number `median_lag_days` (1dp). Dates: first 30+ DPD snapshot_date vs first activity_date >= it.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q10 &nbsp; ★★★ &nbsp; (challenge)

Did hardship work? For non-COVID hardship arrangements that ended by 2025-06-30, compare the % of loans 30+ DPD 6 months after `end_date` (use the snapshot at `last_day(end_date + INTERVAL 6 MONTH)`; loan still non-closed). `arrangements_measured`, `pct_30plus_after_6m` (1dp).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Escalation path: for loans that entered recovery ('Entered recovery - possession process' event), count how many had a 'Legal referral' and a 'Possession notice' in collections beforehand (activity_date < event_date), vs total entering recovery. `entered_recovery`, `with_legal`, `with_possession_notice`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Agent workload: for collections agents (`agent_staff_id`) in 2025, activities per agent and the promise-kept rate (1dp). Show the top 5 agents by activity count. `agent_staff_id`, `activities`, `kept_pct`; sorted by activities descending then id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

COVID deferral cohort: loans with a COVID-19 deferral - how many were 30+ DPD at 2025-12-31 (non-closed), out of how many are live at 2025-12-31? `covid_live_loans`, `now_30plus`, `pct` (1dp).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

Complaint conduct: hardship-handling and collections-conduct complaints per year and the median days to resolve (resolved only, 1dp). `yr`, `complaints`, `median_days_to_resolve`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★ &nbsp; (core)

Hardship type `'COVID-19 repayment deferral'`: arrangements, average planned length (1 dp months), and outcome counts for completed arrangements (`returned`, `arrears`, `closed`). `arrangements`, `avg_planned`, `returned`, `arrears`, `closed`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q16 &nbsp; ★★ &nbsp; (core)

Hardship type `'Reduced repayments'`: arrangements, average planned length (1 dp months), and outcome counts for completed arrangements (`returned`, `arrears`, `closed`). `arrangements`, `avg_planned`, `returned`, `arrears`, `closed`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★★ &nbsp; (core)

Hardship type `'Repayment deferral'`: arrangements, average planned length (1 dp months), and outcome counts for completed arrangements (`returned`, `arrears`, `closed`). `arrangements`, `avg_planned`, `returned`, `arrears`, `closed`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★ &nbsp; (core)

Hardship type `'Interest-only period'`: arrangements, average planned length (1 dp months), and outcome counts for completed arrangements (`returned`, `arrears`, `closed`). `arrangements`, `avg_planned`, `returned`, `arrears`, `closed`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★★ &nbsp; (core)

Hardship type `'Term extension'`: arrangements, average planned length (1 dp months), and outcome counts for completed arrangements (`returned`, `arrears`, `closed`). `arrangements`, `avg_planned`, `returned`, `arrears`, `closed`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★★ &nbsp; (core)

Hardship type `'Arrears capitalisation'`: arrangements, average planned length (1 dp months), and outcome counts for completed arrangements (`returned`, `arrears`, `closed`). `arrangements`, `avg_planned`, `returned`, `arrears`, `closed`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★ &nbsp; (core)

Collections in 2019: activities, distinct loans contacted, promises made and the promise-kept rate (1 dp %). `activities`, `loans`, `promises`, `kept_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★ &nbsp; (core)

Collections in 2020: activities, distinct loans contacted, promises made and the promise-kept rate (1 dp %). `activities`, `loans`, `promises`, `kept_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★ &nbsp; (core)

Collections in 2021: activities, distinct loans contacted, promises made and the promise-kept rate (1 dp %). `activities`, `loans`, `promises`, `kept_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★★ &nbsp; (core)

Collections in 2022: activities, distinct loans contacted, promises made and the promise-kept rate (1 dp %). `activities`, `loans`, `promises`, `kept_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★★ &nbsp; (core)

Collections in 2023: activities, distinct loans contacted, promises made and the promise-kept rate (1 dp %). `activities`, `loans`, `promises`, `kept_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★★ &nbsp; (core)

Collections in 2024: activities, distinct loans contacted, promises made and the promise-kept rate (1 dp %). `activities`, `loans`, `promises`, `kept_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★★ &nbsp; (core)

Collections in 2025: activities, distinct loans contacted, promises made and the promise-kept rate (1 dp %). `activities`, `loans`, `promises`, `kept_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★★ &nbsp; (core)

Activity `'Outbound call'`: count, average `days_past_due_at_activity` (1 dp), and the most common `outcome`. `n`, `avg_dpd`, `top_outcome`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★★ &nbsp; (core)

Activity `'Default notice'`: count, average `days_past_due_at_activity` (1 dp), and the most common `outcome`. `n`, `avg_dpd`, `top_outcome`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★★ &nbsp; (core)

Activity `'SMS reminder'`: count, average `days_past_due_at_activity` (1 dp), and the most common `outcome`. `n`, `avg_dpd`, `top_outcome`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q31 &nbsp; ★★ &nbsp; (core)

Activity `'Legal referral'`: count, average `days_past_due_at_activity` (1 dp), and the most common `outcome`. `n`, `avg_dpd`, `top_outcome`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q32 &nbsp; ★★ &nbsp; (core)

Activity `'Field visit'`: count, average `days_past_due_at_activity` (1 dp), and the most common `outcome`. `n`, `avg_dpd`, `top_outcome`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q33 &nbsp; ★★ &nbsp; (core)

Activity `'Possession notice'`: count, average `days_past_due_at_activity` (1 dp), and the most common `outcome`. `n`, `avg_dpd`, `top_outcome`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q34 &nbsp; ★★ &nbsp; (core)

Activity `'Arrears letter'`: count, average `days_past_due_at_activity` (1 dp), and the most common `outcome`. `n`, `avg_dpd`, `top_outcome`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q35 &nbsp; ★★ &nbsp; (core)

Activity `'Formal demand letter'`: count, average `days_past_due_at_activity` (1 dp), and the most common `outcome`. `n`, `avg_dpd`, `top_outcome`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q36 &nbsp; ★★ &nbsp; (core)

Activity `'Email reminder'`: count, average `days_past_due_at_activity` (1 dp), and the most common `outcome`. `n`, `avg_dpd`, `top_outcome`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q37 &nbsp; ★★★ &nbsp; (challenge)

Complaints received in 2019: count, resolved count, median days to resolve (1 dp) and total compensation (0 dp). `received`, `resolved`, `median_days`, `compensation`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q38 &nbsp; ★★★ &nbsp; (challenge)

Complaints received in 2020: count, resolved count, median days to resolve (1 dp) and total compensation (0 dp). `received`, `resolved`, `median_days`, `compensation`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q39 &nbsp; ★★★ &nbsp; (challenge)

Complaints received in 2021: count, resolved count, median days to resolve (1 dp) and total compensation (0 dp). `received`, `resolved`, `median_days`, `compensation`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q40 &nbsp; ★★★ &nbsp; (challenge)

Complaints received in 2022: count, resolved count, median days to resolve (1 dp) and total compensation (0 dp). `received`, `resolved`, `median_days`, `compensation`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q41 &nbsp; ★★★ &nbsp; (challenge)

Complaints received in 2023: count, resolved count, median days to resolve (1 dp) and total compensation (0 dp). `received`, `resolved`, `median_days`, `compensation`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q42 &nbsp; ★★★ &nbsp; (challenge)

Complaints received in 2024: count, resolved count, median days to resolve (1 dp) and total compensation (0 dp). `received`, `resolved`, `median_days`, `compensation`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q43 &nbsp; ★★★ &nbsp; (challenge)

Complaints received in 2025: count, resolved count, median days to resolve (1 dp) and total compensation (0 dp). `received`, `resolved`, `median_days`, `compensation`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.
