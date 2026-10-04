from ._gen import *
MORE_FOR = 'cr08_hardship_collections'
PROBLEMS = []
for h in ['COVID-19 repayment deferral','Reduced repayments','Repayment deferral','Interest-only period','Term extension','Arrears capitalisation']:
    PROBLEMS.append(P(2, f"Hardship type `'{h}'`: arrangements, average planned length (1 dp months), and outcome counts for completed arrangements (`returned`, `arrears`, `closed`). `arrangements`, `avg_planned`, `returned`, `arrears`, `closed`.",
      f"SELECT COUNT(*), ROUND(AVG(planned_length_months),1), COUNT(*) FILTER (WHERE arrangement_outcome='Returned to normal repayments'), COUNT(*) FILTER (WHERE arrangement_outcome='Moved into arrears'), COUNT(*) FILTER (WHERE arrangement_outcome='Loan closed during arrangement') FROM hardship_arrangement WHERE hardship_type='{h}'"))
for y in range(2019,2026):
    PROBLEMS.append(P(2, f"Collections in {y}: activities, distinct loans contacted, promises made and the promise-kept rate (1 dp %). `activities`, `loans`, `promises`, `kept_pct`.",
      f"SELECT COUNT(*), COUNT(DISTINCT loan_id), COUNT(*) FILTER (WHERE promise_amount IS NOT NULL), ROUND(100.0*COUNT(*) FILTER (WHERE promise_kept_flag)/NULLIF(COUNT(*) FILTER (WHERE promise_amount IS NOT NULL),0),1) FROM collections_activity WHERE {yr('activity_date',y)}"))
ACT = ['Outbound call','Default notice','SMS reminder','Legal referral','Field visit','Possession notice','Arrears letter','Formal demand letter','Email reminder']
for a in ACT:
    PROBLEMS.append(P(2, f"Activity `'{a}'`: count, average `days_past_due_at_activity` (1 dp), and the most common `outcome`. `n`, `avg_dpd`, `top_outcome`.",
      f"SELECT COUNT(*), ROUND(AVG(days_past_due_at_activity),1), (SELECT outcome FROM collections_activity WHERE activity_type='{a}' GROUP BY 1 ORDER BY COUNT(*) DESC, 1 LIMIT 1) FROM collections_activity WHERE activity_type='{a}'"))
for y in range(2019,2026):
    PROBLEMS.append(P(3, f"Complaints received in {y}: count, resolved count, median days to resolve (1 dp) and total compensation (0 dp). `received`, `resolved`, `median_days`, `compensation`.",
      f"SELECT COUNT(*), COUNT(resolved_date), ROUND(MEDIAN(resolved_date-received_date),1), ROUND(SUM(COALESCE(compensation_amount,0)),0) FROM complaint WHERE {yr('received_date',y)}"))
