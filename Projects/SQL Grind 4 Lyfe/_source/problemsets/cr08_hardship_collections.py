from . import P

PRIMER = r"""
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
"""

CONCEPT = dict(id="cr08_hardship_collections", title="CR08 - Hardship and collections", primer=PRIMER, problems=[
    P(1, "Hardship arrangements by type and status: `hardship_type`, `arrangements`, `still_active` (status Active); sorted by arrangements descending then type.",
      "SELECT hardship_type, COUNT(*) AS n, COUNT(*) FILTER (WHERE arrangement_status='Active') FROM hardship_arrangement GROUP BY 1 ORDER BY n DESC, 1"),
    P(1, "Hardship arrangements started per year. `yr`, `arrangements`; sorted by year.",
      "SELECT year(start_date), COUNT(*) FROM hardship_arrangement GROUP BY 1 ORDER BY 1"),
    P(1, "Collections activity volume by `activity_type`. `activity_type`, `n`; sorted by n descending then type.",
      "SELECT activity_type, COUNT(*) AS n FROM collections_activity GROUP BY 1 ORDER BY n DESC, 1"),
    P(2, "Non-COVID hardship outcomes: for arrangements that are `Completed` and not COVID-19 deferrals, the % with each outcome. `arrangement_outcome`, `n`, `pct` (1dp); sorted by n descending then outcome.",
      "SELECT arrangement_outcome, COUNT(*) AS n, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (),1) FROM hardship_arrangement WHERE arrangement_status='Completed' AND hardship_type<>'COVID-19 repayment deferral' GROUP BY 1 ORDER BY n DESC, 1"),
    P(2, "Promise-to-pay performance: of promises (`promise_amount` not null), the % kept (`promise_kept_flag`) by `activity_type` (1dp). `activity_type`, `promises`, `kept_pct`; sorted by activity type.",
      "SELECT activity_type, COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE promise_kept_flag)/COUNT(*),1) FROM collections_activity WHERE promise_amount IS NOT NULL GROUP BY 1 ORDER BY 1"),
    P(2, "Average planned arrangement length in months (1dp) by hardship type for non-COVID types. `hardship_type`, `avg_planned_months`; sorted by type.",
      "SELECT hardship_type, ROUND(AVG(planned_length_months),1) FROM hardship_arrangement WHERE hardship_type<>'COVID-19 repayment deferral' GROUP BY 1 ORDER BY 1"),
    P(2, "Collections contacts per loan: distribution of the number of activity rows per loan: `contacts_bucket` (`1-3`, `4-10`, `11+`), `loans`; sorted by bucket's lower bound.",
      "SELECT b, COUNT(*) FROM (SELECT CASE WHEN n<=3 THEN '1-3' WHEN n<=10 THEN '4-10' ELSE '11+' END AS b, CASE WHEN n<=3 THEN 1 WHEN n<=10 THEN 2 ELSE 3 END AS k FROM (SELECT loan_id, COUNT(*) AS n FROM collections_activity GROUP BY 1)) GROUP BY b, k ORDER BY k"),
    P(2, "Dishonoured payments: `loan_payment` rows with `payment_status = 'Dishonoured'` by `failure_reason`. `failure_reason`, `n`; sorted by n descending then reason.",
      "SELECT failure_reason, COUNT(*) AS n FROM loan_payment WHERE payment_status='Dishonoured' GROUP BY 1 ORDER BY n DESC, 1"),
    P(3, "First contact lag: for each loan, days from the first snapshot where dpd >= 30 to its first `collections_activity` on or after that date. Median lag (days) across loans that have both. One number `median_lag_days` (1dp). Dates: first 30+ DPD snapshot_date vs first activity_date >= it.",
      """WITH f AS (SELECT loan_id, MIN(snapshot_date) AS d FROM loan_monthly_snapshot WHERE days_past_due>=30 GROUP BY 1),
c AS (SELECT f.loan_id, f.d, MIN(a.activity_date) AS ca FROM f JOIN collections_activity a ON a.loan_id=f.loan_id AND a.activity_date>=f.d GROUP BY 1,2)
SELECT ROUND(MEDIAN(ca-d),1) FROM c"""),
    P(3, "Did hardship work? For non-COVID hardship arrangements that ended by 2025-06-30, compare the % of loans 30+ DPD 6 months after `end_date` (use the snapshot at `last_day(end_date + INTERVAL 6 MONTH)`; loan still non-closed). `arrangements_measured`, `pct_30plus_after_6m` (1dp).",
      """SELECT COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=30)/COUNT(*),1) FROM hardship_arrangement h JOIN loan_monthly_snapshot s ON s.loan_id=h.loan_id AND s.snapshot_date=last_day(h.end_date + INTERVAL 6 MONTH)
WHERE h.hardship_type<>'COVID-19 repayment deferral' AND h.end_date<=DATE '2025-06-30' AND s.loan_status<>'Closed'"""),
    P(3, "Escalation path: for loans that entered recovery ('Entered recovery - possession process' event), count how many had a 'Legal referral' and a 'Possession notice' in collections beforehand (activity_date < event_date), vs total entering recovery. `entered_recovery`, `with_legal`, `with_possession_notice`.",
      """WITH r AS (SELECT loan_id, MIN(event_date) AS d FROM loan_event WHERE event_type='Entered recovery - possession process' GROUP BY 1)
SELECT COUNT(*), COUNT(*) FILTER (WHERE EXISTS (SELECT 1 FROM collections_activity a WHERE a.loan_id=r.loan_id AND a.activity_type='Legal referral' AND a.activity_date<r.d)), COUNT(*) FILTER (WHERE EXISTS (SELECT 1 FROM collections_activity a WHERE a.loan_id=r.loan_id AND a.activity_type='Possession notice' AND a.activity_date<r.d)) FROM r"""),
    P(3, "Agent workload: for collections agents (`agent_staff_id`) in 2025, activities per agent and the promise-kept rate (1dp). Show the top 5 agents by activity count. `agent_staff_id`, `activities`, `kept_pct`; sorted by activities descending then id.",
      "SELECT agent_staff_id, COUNT(*) AS n, ROUND(100.0*COUNT(*) FILTER (WHERE promise_kept_flag)/NULLIF(COUNT(*) FILTER (WHERE promise_amount IS NOT NULL),0),1) FROM collections_activity WHERE activity_date>=DATE '2025-01-01' AND activity_date<DATE '2026-01-01' AND agent_staff_id IS NOT NULL GROUP BY 1 ORDER BY n DESC, 1 LIMIT 5"),
    P(3, "COVID deferral cohort: loans with a COVID-19 deferral - how many were 30+ DPD at 2025-12-31 (non-closed), out of how many are live at 2025-12-31? `covid_live_loans`, `now_30plus`, `pct` (1dp).",
      "SELECT COUNT(*), COUNT(*) FILTER (WHERE s.days_past_due>=30), ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=30)/COUNT(*),1) FROM loan_monthly_snapshot s WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' AND EXISTS (SELECT 1 FROM hardship_arrangement h WHERE h.loan_id=s.loan_id AND h.hardship_type='COVID-19 repayment deferral')"),
    P(3, "Complaint conduct: hardship-handling and collections-conduct complaints per year and the median days to resolve (resolved only, 1dp). `yr`, `complaints`, `median_days_to_resolve`; sorted by year.",
      "SELECT year(received_date), COUNT(*), ROUND(MEDIAN(resolved_date-received_date),1) FROM complaint WHERE category IN ('Hardship handling','Collections conduct') GROUP BY 1 ORDER BY 1"),
])
