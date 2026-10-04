from . import P

PRIMER = r"""
## Scenario: are newer loans performing worse than older ones?

**Vintage analysis** compares cohorts at the SAME AGE (months on book, MOB), not the same calendar date - so a 2023 loan at MOB 12 is compared with a 2021 loan at MOB 12.

```
   % 30+ DPD
     |        2023 vintage  /
     |      ------------ /  <- worse than 2021 at same age = tighter-than-it-should-have-been underwriting? or rate shock?
     |   2021 ........
     +-----------------------> months on book
```

Pattern:
```
 SELECT year(l.origination_date) AS vintage, s.months_on_book AS mob,
        COUNT(*) AS loans, COUNT(*) FILTER (WHERE s.days_past_due >= 30) AS bad
 FROM loan_monthly_snapshot s JOIN loan l USING (loan_id)
 GROUP BY 1, 2
```
Pay attention to the **denominator**: which loans are still observable at that MOB? Closed loans drop out (survivorship), and young vintages have no data for high MOBs.
"""

CONCEPT = dict(id="cr04_vintage_analysis", title="CR04 - Vintage and cohort credit performance", primer=PRIMER, problems=[
    P(1, "Loans originated per year and their average original amount (0dp). `yr`, `loans`, `avg_amount`; sorted by year.",
      "SELECT year(origination_date), COUNT(*), ROUND(AVG(original_amount),0) FROM loan GROUP BY 1 ORDER BY 1"),
    P(1, "Average origination LVR (1dp) and average interest rate (2dp) by origination year. `yr`, `avg_lvr`, `avg_rate`; sorted by year.",
      "SELECT year(origination_date), ROUND(AVG(lvr_at_origination_pct),1), ROUND(AVG(interest_rate_at_origination_pct),2) FROM loan GROUP BY 1 ORDER BY 1"),
    P(2, "30+ DPD rate at MOB 6 (count basis, 2dp, non-closed) by origination year for 2019-2025. `yr`, `loans`, `pct_30plus`; sorted by year.",
      "SELECT year(l.origination_date), COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=30)/COUNT(*),2) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.months_on_book=6 AND s.loan_status<>'Closed' AND year(l.origination_date) BETWEEN 2019 AND 2025 GROUP BY 1 ORDER BY 1"),
    P(2, "The vintage grid at MOB 3, 6, 12, 24 for origination years 2020-2023: 30+ DPD rate (2dp) laid out as columns. `yr`, `mob3`, `mob6`, `mob12`, `mob24`; sorted by year. Non-closed rows.",
      "SELECT year(l.origination_date), "+", ".join(f"ROUND(100.0*COUNT(*) FILTER (WHERE s.months_on_book={m} AND s.days_past_due>=30)/NULLIF(COUNT(*) FILTER (WHERE s.months_on_book={m}),0),2)" for m in (3,6,12,24))+" FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.loan_status<>'Closed' AND year(l.origination_date) BETWEEN 2020 AND 2023 GROUP BY 1 ORDER BY 1"),
    P(2, "Cumulative ever-90+ by origination year: % of each vintage's loans that have EVER been 90+ DPD (any snapshot, 2dp). `yr`, `loans`, `ever90_pct`; sorted by year. All loans in the vintage are the denominator.",
      "SELECT year(l.origination_date), COUNT(*), ROUND(100.0*COUNT(e.loan_id)/COUNT(*),2) FROM loan l LEFT JOIN (SELECT loan_id FROM loan_monthly_snapshot GROUP BY 1 HAVING MAX(days_past_due)>=90) e ON e.loan_id=l.loan_id GROUP BY 1 ORDER BY 1"),
    P(2, "Attrition curve: % of the 2021 vintage (by loan count) still open at MOB 12, 24, 36, 48 (open = has a non-closed snapshot at that MOB), as % of loans originated in 2021. Return `mob`, `open_pct` (1dp); sorted by mob.",
      "SELECT m.mob, ROUND(100.0*COUNT(DISTINCT s.loan_id)/(SELECT COUNT(*) FROM loan WHERE year(origination_date)=2021),1) FROM (SELECT unnest([12,24,36,48]) AS mob) m LEFT JOIN (SELECT s.loan_id, s.months_on_book FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE year(l.origination_date)=2021 AND s.loan_status<>'Closed') s ON s.months_on_book=m.mob GROUP BY m.mob ORDER BY m.mob"),
    P(3, "Channel quality by vintage: for origination years 2021-2024, the ever-90+ rate (2dp) by channel as columns. `yr`, `broker`, `branch`, `digital`, `mobile`; sorted by year. Denominator = all loans of that vintage/channel.",
      "SELECT year(l.origination_date), "+", ".join(f"ROUND(100.0*COUNT(e.loan_id) FILTER (WHERE l.channel='{c}')/COUNT(*) FILTER (WHERE l.channel='{c}'),2)" for c in ("Broker","Branch","Digital","Mobile Lender"))+" FROM loan l LEFT JOIN (SELECT loan_id FROM loan_monthly_snapshot GROUP BY 1 HAVING MAX(days_past_due)>=90) e ON e.loan_id=l.loan_id WHERE year(l.origination_date) BETWEEN 2021 AND 2024 GROUP BY 1 ORDER BY 1"),
    P(3, "Bureau score at origination vs later default: bucket the primary applicant's `bureau_score` at application (join via `loan.application_id` to `credit_bureau_report` for the primary customer) into `<600`, `600-699`, `700-799`, `800+`, with NULLs as `no score`; return the ever-90+ rate (2dp) per bucket. `score_band`, `loans`, `ever90_pct`; sorted by band label alphabetically.",
      """WITH e AS (SELECT loan_id FROM loan_monthly_snapshot GROUP BY 1 HAVING MAX(days_past_due)>=90)
SELECT band, COUNT(*), ROUND(100.0*COUNT(e.loan_id)/COUNT(*),2) FROM (SELECT l.loan_id, CASE WHEN b.bureau_score IS NULL THEN 'no score' WHEN b.bureau_score<600 THEN '<600' WHEN b.bureau_score<700 THEN '600-699' WHEN b.bureau_score<800 THEN '700-799' ELSE '800+' END AS band
 FROM loan l JOIN credit_bureau_report b ON b.application_id=l.application_id AND b.customer_id=l.primary_customer_id) t LEFT JOIN e USING (loan_id) GROUP BY band ORDER BY band"""),
    P(3, "Policy-epoch performance: using the serviceability policy in force at the application date (`ref_serviceability_policy`), the ever-90+ rate (2dp) per `policy_id` for loans with an `application_id`. `policy_id`, `loans`, `ever90_pct`; sorted by policy_id.",
      """WITH e AS (SELECT loan_id FROM loan_monthly_snapshot GROUP BY 1 HAVING MAX(days_past_due)>=90)
SELECT p.policy_id, COUNT(*), ROUND(100.0*COUNT(e.loan_id)/COUNT(*),2) FROM loan l JOIN loan_application a ON a.application_id=l.application_id JOIN ref_serviceability_policy p ON a.application_date BETWEEN p.effective_from AND COALESCE(p.effective_to, DATE '9999-12-31') LEFT JOIN e ON e.loan_id=l.loan_id GROUP BY 1 ORDER BY 1"""),
    P(3, "Seasoning of arrears: at 2025-12-31, the 30+ DPD rate (count, 2dp) by months-on-book bucket `0-11`, `12-23`, `24-47`, `48+` for live loans. `mob_bucket`, `loans`, `rate_pct`; sorted by bucket's lower bound.",
      "SELECT b, COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE d>=30)/COUNT(*),2) FROM (SELECT days_past_due AS d, CASE WHEN months_on_book<12 THEN '0-11' WHEN months_on_book<24 THEN '12-23' WHEN months_on_book<48 THEN '24-47' ELSE '48+' END AS b, CASE WHEN months_on_book<12 THEN 1 WHEN months_on_book<24 THEN 2 WHEN months_on_book<48 THEN 3 ELSE 4 END AS k FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed') GROUP BY b, k ORDER BY k"),
    P(3, "First-year failures: loans that reached 30+ DPD within their first 6 months (MOB <= 6) - 'early payment defaults' - as a % of loans originated, by origination year (2019-2024, 2dp). `yr`, `loans`, `epd_pct`; sorted by year.",
      "SELECT year(l.origination_date), COUNT(*), ROUND(100.0*COUNT(e.loan_id)/COUNT(*),2) FROM loan l LEFT JOIN (SELECT DISTINCT loan_id FROM loan_monthly_snapshot WHERE months_on_book<=6 AND days_past_due>=30) e ON e.loan_id=l.loan_id WHERE year(l.origination_date) BETWEEN 2019 AND 2024 GROUP BY 1 ORDER BY 1"),
])
