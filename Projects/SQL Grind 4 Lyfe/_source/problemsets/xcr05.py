from ._gen import *
MORE_FOR = 'cr05_origination_underwriting'
PROBLEMS = []
for y in YEARS:
    PROBLEMS.append(P(1, f"Funnel for applications lodged in {y}: lodged, decided, approved, settled and the settle rate of lodged (1 dp %). `lodged`, `decided`, `approved`, `settled`, `settle_pct`.",
      f"SELECT COUNT(*), COUNT(decision), COUNT(*) FILTER (WHERE decision='Approved'), COUNT(*) FILTER (WHERE current_status='Settled'), ROUND(100.0*COUNT(*) FILTER (WHERE current_status='Settled')/COUNT(*),1) FROM loan_application WHERE {yr('application_date',y)}"))
for c in CHANNELS:
    PROBLEMS.append(P(2, f"Decline reasons for `'{c}'` applications: `reason_description`, `declines`, `share_pct` (of the channel's declines, 1 dp); sorted by declines descending then description.",
      f"SELECT r.reason_description, COUNT(*) AS n, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (),1) FROM loan_application a JOIN ref_decline_reason r ON r.reason_code=a.decline_reason_code WHERE a.channel='{c}' AND a.decision='Declined' GROUP BY 1 ORDER BY n DESC, 1"))
for y in YEARS:
    PROBLEMS.append(P(2, f"Applications lodged in {y} with assessments: average NSR (2 dp), average DTI (2 dp), % with HEM applied (1 dp). `avg_nsr`, `avg_dti`, `hem_pct`.",
      f"SELECT ROUND(AVG(s.nsr),2), ROUND(AVG(s.dti_ratio),2), ROUND(100.0*COUNT(*) FILTER (WHERE s.hem_applied_flag)/COUNT(*),1) FROM loan_application a JOIN application_assessment s USING (application_id) WHERE {yr('a.application_date',y)}"))
for y in YEARS:
    PROBLEMS.append(P(3, f"Policy exceptions in {y}: approved applications, those with a policy exception, the exception rate (2 dp %) and the most common exception reason. `approved`, `exceptions`, `exception_pct`, `top_reason`.",
      f"SELECT COUNT(*), COUNT(*) FILTER (WHERE policy_exception_flag), ROUND(100.0*COUNT(*) FILTER (WHERE policy_exception_flag)/COUNT(*),2), (SELECT policy_exception_reason FROM loan_application WHERE decision='Approved' AND policy_exception_flag AND {yr('application_date',y)} GROUP BY 1 ORDER BY COUNT(*) DESC, 1 LIMIT 1) FROM loan_application WHERE decision='Approved' AND {yr('application_date',y)}"))
for ch in CHANNELS:
    PROBLEMS.append(P(3, f"`'{ch}'` channel: approval rate (decided only, 1 dp %) for each year 2019-2025. `yr`, `approval_pct`; sorted by year.",
      f"SELECT year(application_date), ROUND(100.0*COUNT(*) FILTER (WHERE decision='Approved')/COUNT(decision),1) FROM loan_application WHERE channel='{ch}' GROUP BY 1 ORDER BY 1"))
