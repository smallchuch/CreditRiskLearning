from . import P

PRIMER = r"""
## Scenario: origination funnel and underwriting quality

Applications flow through **lodged -> assessed -> decided -> settled**. The credit team asks: where do we lose people, why do we decline them, and are we approving risky ones?

```
 Lodged  ->  Decided  ->  Approved  ->  Settled
  100%        ~85%         ~60%          ~55%      <- typical funnel shape
```

Key columns: `loan_application` (status, decision, decline reason, exception flag), `application_assessment` (the serviceability workings):
* **NSR** (net serviceability ratio) = assessed net income / assessed commitments. Policy minimum lives in `ref_serviceability_policy.min_nsr`.
* **DTI** = total debt after settlement / gross income (`dti_ratio`).
* **HEM** = household expenditure measure (benchmark living costs); `hem_applied_flag` = benchmark used instead of declared expenses.
* `buffer_pct`: serviceability buffer added to the rate (2.5-3%) per policy epoch.
* **Policy exception** = approved despite breaching a rule (`policy_exception_flag`, `policy_exception_reason`).
"""

CONCEPT = dict(id="cr05_origination_underwriting", title="CR05 - Origination funnel, serviceability and underwriting", primer=PRIMER, problems=[
    P(1, "Funnel counts for 2025: applications lodged in 2025, how many decided (decision not null), approved, settled (`current_status='Settled'`). One row: `lodged`, `decided`, `approved`, `settled`.",
      "SELECT COUNT(*), COUNT(decision), COUNT(*) FILTER (WHERE decision='Approved'), COUNT(*) FILTER (WHERE current_status='Settled') FROM loan_application WHERE application_date>=DATE '2025-01-01' AND application_date<DATE '2026-01-01'"),
    P(1, "Decline reasons (with description) for 2025 declines: `reason_description`, `declines`; sorted by declines descending then description.",
      "SELECT r.reason_description, COUNT(*) AS n FROM loan_application a JOIN ref_decline_reason r ON r.reason_code=a.decline_reason_code WHERE a.application_date>=DATE '2025-01-01' AND a.decision='Declined' GROUP BY 1 ORDER BY n DESC, 1"),
    P(1, "Average assessed NSR and DTI (2dp each) across all application assessments. Two numbers: `avg_nsr`, `avg_dti`.",
      "SELECT ROUND(AVG(nsr),2), ROUND(AVG(dti_ratio),2) FROM application_assessment"),
    P(2, "Approval rate by year (decided apps only, 1dp): `yr`, `approval_pct`; sorted by year (application year).",
      "SELECT year(application_date), ROUND(100.0*COUNT(*) FILTER (WHERE decision='Approved')/COUNT(decision),1) FROM loan_application GROUP BY 1 ORDER BY 1"),
    P(2, "Serviceability declines by policy epoch: for applications declined with code 'SERV', the count per `policy_id` (range join application_date to policy). `policy_id`, `serv_declines`; sorted by policy.",
      "SELECT p.policy_id, COUNT(*) FROM loan_application a JOIN ref_serviceability_policy p ON a.application_date BETWEEN p.effective_from AND COALESCE(p.effective_to,DATE '9999-12-31') WHERE a.decline_reason_code='SERV' GROUP BY 1 ORDER BY 1"),
    P(2, "Approved applications where the assessed NSR is below the policy minimum (`ref_serviceability_policy.min_nsr` for the epoch of the application) - i.e. approved below the minimum. Count them. One number (policy exceptions may explain them).",
      "SELECT COUNT(*) FROM loan_application a JOIN application_assessment s USING (application_id) JOIN ref_serviceability_policy p ON a.application_date BETWEEN p.effective_from AND COALESCE(p.effective_to,DATE '9999-12-31') WHERE a.decision='Approved' AND s.nsr < p.min_nsr"),
    P(2, "Of those below-minimum approvals, how many carry a `policy_exception_flag`? Return `below_min_approved`, `with_exception`, `without_exception`.",
      "SELECT COUNT(*), COUNT(*) FILTER (WHERE a.policy_exception_flag), COUNT(*) FILTER (WHERE NOT a.policy_exception_flag) FROM loan_application a JOIN application_assessment s USING (application_id) JOIN ref_serviceability_policy p ON a.application_date BETWEEN p.effective_from AND COALESCE(p.effective_to,DATE '9999-12-31') WHERE a.decision='Approved' AND s.nsr < p.min_nsr"),
    P(2, "HEM usage: % of assessments where the HEM benchmark was applied (`hem_applied_flag`), by application year (1dp). `yr`, `hem_pct`; sorted by year.",
      "SELECT year(a.application_date), ROUND(100.0*COUNT(*) FILTER (WHERE s.hem_applied_flag)/COUNT(*),1) FROM loan_application a JOIN application_assessment s USING (application_id) GROUP BY 1 ORDER BY 1"),
    P(2, "High DTI lending: approved applications with `dti_ratio >= 6`: counts by year of application. `yr`, `high_dti_approvals`; sorted by year.",
      "SELECT year(a.application_date), COUNT(*) FROM loan_application a JOIN application_assessment s USING (application_id) WHERE a.decision='Approved' AND s.dti_ratio>=6 GROUP BY 1 ORDER BY 1"),
    P(2, "Time-to-decision by channel (median days, 1dp) for decided applications. `channel`, `median_days`; sorted by channel.",
      "SELECT channel, ROUND(MEDIAN(decision_date-application_date),1) FROM loan_application WHERE decision_date IS NOT NULL GROUP BY 1 ORDER BY 1"),
    P(3, "Assessor outcomes: for assessors with at least 500 decided applications, the approval rate (1dp) and exception rate among approvals (1dp). `assessor_staff_id`, `decided`, `approval_pct`, `exception_pct`; sorted by `decided` descending then id. Top 10 rows.",
      "SELECT assessor_staff_id, COUNT(decision) AS d, ROUND(100.0*COUNT(*) FILTER (WHERE decision='Approved')/COUNT(decision),1), ROUND(100.0*COUNT(*) FILTER (WHERE decision='Approved' AND policy_exception_flag)/NULLIF(COUNT(*) FILTER (WHERE decision='Approved'),0),1) FROM loan_application GROUP BY 1 HAVING COUNT(decision)>=500 ORDER BY d DESC, 1 LIMIT 10"),
    P(3, "Resizing: for applications that became loans, the share where the loan `original_amount` is below `requested_amount` (cut down by credit) - by channel (1dp %). `channel`, `resized_pct`; sorted by channel. Use a 1-dollar tolerance.",
      "SELECT a.channel, ROUND(100.0*COUNT(*) FILTER (WHERE l.original_amount < a.requested_amount-1)/COUNT(*),1) FROM loan l JOIN loan_application a ON a.application_id=l.application_id GROUP BY 1 ORDER BY 1"),
    P(3, "Resubmission funnel: of applications that were declined, how many were followed by a resubmission (some later application has `resubmission_of_application_id` = this one), and how many of those resubmissions were approved? `declined`, `resubmitted`, `resubmitted_approved`.",
      "SELECT (SELECT COUNT(*) FROM loan_application WHERE decision='Declined'), (SELECT COUNT(*) FROM loan_application d WHERE d.decision='Declined' AND EXISTS (SELECT 1 FROM loan_application r WHERE r.resubmission_of_application_id=d.application_id)), (SELECT COUNT(*) FROM loan_application d WHERE d.decision='Declined' AND EXISTS (SELECT 1 FROM loan_application r WHERE r.resubmission_of_application_id=d.application_id AND r.decision='Approved'))"),
    P(3, "Income verification: for approved applications in 2025, the % whose total `declared_annual_amount` differs from total verified (verified NULL treated as the declared value) by more than 5% - overstated income. One number (2dp). Aggregate income per application first.",
      """WITH i AS (SELECT application_id, SUM(declared_annual_amount) AS dec, SUM(COALESCE(verified_annual_amount, declared_annual_amount)) AS ver FROM applicant_income GROUP BY 1)
SELECT ROUND(100.0*COUNT(*) FILTER (WHERE i.dec > i.ver*1.05)/COUNT(*),2) FROM loan_application a JOIN i USING (application_id) WHERE a.decision='Approved' AND a.application_date>=DATE '2025-01-01' AND a.application_date<DATE '2026-01-01'"""),
    P(3, "Broker accreditation compliance: applications lodged via a broker where the application_date is BEFORE the broker's `accreditation_date` (should be 0). Count them. One number.",
      "SELECT COUNT(*) FROM loan_application a JOIN dim_broker b ON b.broker_id=a.broker_id WHERE a.application_date < b.accreditation_date"),
])
