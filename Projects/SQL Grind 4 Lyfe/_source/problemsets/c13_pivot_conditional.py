from . import P

PRIMER = r"""
## Turn rows into columns (pivot) with conditional aggregation

```
 long (tall)                      wide (pivoted)
 year  purpose   n                year | Refi | Constr | ...
 2023  Refi      900              2023 |  900 |   300
 2023  Constr    300              2024 | ...
```

The portable way:
```
 SELECT year(origination_date) AS yr,
        COUNT(*) FILTER (WHERE purpose = 'Refinance')    AS refi,
        COUNT(*) FILTER (WHERE purpose = 'Construction') AS constr
 FROM loan GROUP BY 1
```
(`SUM(CASE WHEN ... THEN 1 ELSE 0 END)` does the same in every SQL dialect - learn both.)

DuckDB also has `PIVOT loan ON purpose USING COUNT(*) GROUP BY year(...)` and `UNPIVOT` (wide -> long).

Rates and ratios: `AVG(CASE WHEN cond THEN 1.0 ELSE 0 END)` = share meeting `cond`. Use this to build default rates, approval rates, cure rates in one pass.
"""

CONCEPT = dict(id="13_pivot_conditional", title="13 - Pivoting and conditional aggregation", primer=PRIMER, problems=[
    P(1, "Loans per year as columns by `rate_type`: `yr`, `fixed`, `variable` counts; sorted by `yr`.",
      "SELECT year(origination_date), COUNT(*) FILTER (WHERE rate_type='Fixed'), COUNT(*) FILTER (WHERE rate_type='Variable') FROM loan GROUP BY 1 ORDER BY 1"),
    P(1, "Per `channel`: counts of Active, Closed and In Recovery loans as three columns. Return `channel`, `active`, `closed`, `in_recovery`; sorted by `channel`.",
      "SELECT channel, COUNT(*) FILTER (WHERE loan_status='Active'), COUNT(*) FILTER (WHERE loan_status='Closed'), COUNT(*) FILTER (WHERE loan_status='In Recovery') FROM loan GROUP BY 1 ORDER BY 1"),
    P(1, "Use DuckDB `PIVOT` (list the values with `ON col IN (...)`): loans by `channel` (rows) and `loan_status` (columns). Return the pivoted result; columns order will be alphabetical: `channel`, Active, Closed, In Recovery; sorted by `channel`.",
      "SELECT * FROM (PIVOT loan ON loan_status IN ('Active','Closed','In Recovery') USING COUNT(*) GROUP BY channel) ORDER BY channel"),
    P(2, "Application outcomes by year: `yr`, `settled`, `declined`, `withdrawn`, `lapsed`. Sorted by `yr` (year of application_date).",
      "SELECT year(application_date), COUNT(*) FILTER (WHERE current_status='Settled'), COUNT(*) FILTER (WHERE current_status='Declined'), COUNT(*) FILTER (WHERE current_status='Withdrawn'), COUNT(*) FILTER (WHERE current_status='Lapsed') FROM loan_application GROUP BY 1 ORDER BY 1"),
    P(2, "Approval and decline rates by `channel` in one query. Among decided applications: `approved_pct`, `declined_pct` (1dp each). Return `channel`, `approved_pct`, `declined_pct`; sorted by `channel`.",
      "SELECT channel, ROUND(100.0*COUNT(*) FILTER (WHERE decision='Approved')/COUNT(decision),1), ROUND(100.0*COUNT(*) FILTER (WHERE decision='Declined')/COUNT(decision),1) FROM loan_application GROUP BY 1 ORDER BY 1"),
    P(2, "Decline reasons as columns for 'SERV', 'CRED', 'POLICY', 'LVR' by `channel` (counts). Return `channel`, `serv`, `cred`, `policy`, `lvr`; sorted by `channel`.",
      "SELECT channel, COUNT(*) FILTER (WHERE decline_reason_code='SERV'), COUNT(*) FILTER (WHERE decline_reason_code='CRED'), COUNT(*) FILTER (WHERE decline_reason_code='POLICY'), COUNT(*) FILTER (WHERE decline_reason_code='LVR') FROM loan_application GROUP BY 1 ORDER BY 1"),
    P(2, "LVR band x purpose matrix: for loans, count by LVR band (`<=60`, `60-80`, `80-90`, `>90` using CASE) as columns, per `purpose` as rows. Return `purpose`, `le60`, `b60_80`, `b80_90`, `gt90`; sorted by `purpose`. Upper bounds inclusive (a loan at exactly 80 belongs to 60-80).",
      "SELECT purpose, COUNT(*) FILTER (WHERE lvr_at_origination_pct<=60), COUNT(*) FILTER (WHERE lvr_at_origination_pct>60 AND lvr_at_origination_pct<=80), COUNT(*) FILTER (WHERE lvr_at_origination_pct>80 AND lvr_at_origination_pct<=90), COUNT(*) FILTER (WHERE lvr_at_origination_pct>90) FROM loan GROUP BY 1 ORDER BY 1"),
    P(2, "Arrears matrix at 2025-12-31 (non-closed): `repayment_type` rows; columns: `current` (dpd 0), `d1_29`, `d30_89`, `d90plus`, as loan counts. Sorted by `repayment_type`.",
      "SELECT repayment_type, COUNT(*) FILTER (WHERE days_past_due=0), COUNT(*) FILTER (WHERE days_past_due BETWEEN 1 AND 29), COUNT(*) FILTER (WHERE days_past_due BETWEEN 30 AND 89), COUNT(*) FILTER (WHERE days_past_due>=90) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(2, "UNPIVOT by hand: from a one-row summary of loan counts (`active`, `closed`, `in_recovery`) produce a tall table `status`, `n` using UNION ALL of three selects. Sorted by `status`.",
      "SELECT status, n FROM (SELECT 'active' AS status, COUNT(*) AS n FROM loan WHERE loan_status='Active' UNION ALL SELECT 'closed', COUNT(*) FROM loan WHERE loan_status='Closed' UNION ALL SELECT 'in_recovery', COUNT(*) FROM loan WHERE loan_status='In Recovery') ORDER BY 1"),
    P(3, "Default rate by LVR band. Use `ref_lvr_band` to bucket each loan's `lvr_at_origination_pct` (a band holds LVRs above its `lvr_from_pct` up to and including its `lvr_to_pct`; the first band also includes 0; a NULL upper bound means no cap). For each band return `band_name`, `loans`, `ever_90` (loans that were ever 90+ DPD in any snapshot) and `rate_pct` (2dp). Sorted by `band_id`.",
      """WITH e AS (SELECT loan_id FROM loan_monthly_snapshot GROUP BY 1 HAVING MAX(days_past_due)>=90)
SELECT b.band_name, COUNT(*), COUNT(e.loan_id), ROUND(100.0*COUNT(e.loan_id)/COUNT(*),2) FROM loan l JOIN ref_lvr_band b ON (l.lvr_at_origination_pct > b.lvr_from_pct OR b.lvr_from_pct=0) AND l.lvr_at_origination_pct <= COALESCE(b.lvr_to_pct, 1e9) LEFT JOIN e ON e.loan_id=l.loan_id GROUP BY b.band_id, b.band_name ORDER BY b.band_id"""),
    P(3, "Origination mix by year (% of loans): rows = year, columns = share of loans by `channel` (Broker, Branch, Digital, Mobile Lender), 1dp. Return `yr`, `broker_pct`, `branch_pct`, `digital_pct`, `mobile_pct`; sorted by `yr`.",
      "SELECT year(origination_date), ROUND(100.0*COUNT(*) FILTER (WHERE channel='Broker')/COUNT(*),1), ROUND(100.0*COUNT(*) FILTER (WHERE channel='Branch')/COUNT(*),1), ROUND(100.0*COUNT(*) FILTER (WHERE channel='Digital')/COUNT(*),1), ROUND(100.0*COUNT(*) FILTER (WHERE channel='Mobile Lender')/COUNT(*),1) FROM loan GROUP BY 1 ORDER BY 1"),
    P(3, "Stage migration table (ECL): per `ifrs9_stage` at 2025-12-31 (the last `reporting_date` in `ecl_provision_quarterly`): loans, total EAD (0dp), total ECL (0dp), and coverage % = ECL/EAD (2dp). Return `ifrs9_stage`, `loans`, `ead`, `ecl`, `coverage_pct`; sorted by stage.",
      "SELECT ifrs9_stage, COUNT(*), ROUND(SUM(ead),0), ROUND(SUM(ecl_amount),0), ROUND(100*SUM(ecl_amount)/SUM(ead),2) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31' GROUP BY 1 ORDER BY 1"),
    P(3, "Collections outcome grid: activity types (rows) by whether the outcome was `'Promise to pay'` or `'Payment taken'` (columns). Return `activity_type`, `promises`, `payments`, `total`; sorted by `total` descending then type.",
      "SELECT activity_type, COUNT(*) FILTER (WHERE outcome='Promise to pay'), COUNT(*) FILTER (WHERE outcome='Payment taken'), COUNT(*) AS t FROM collections_activity GROUP BY 1 ORDER BY t DESC, 1"),
    P(3, "Pivot the HPI table: for 2025 year-end (`month_end_date = 2025-12-31`) and 2020 year-end (`2020-12-31`), show each state's index in two columns and the growth %. Return `state`, `idx_2020`, `idx_2025`, `growth_pct` (1dp); sorted by `state`.",
      "SELECT state, MAX(price_index) FILTER (WHERE month_end_date=DATE '2020-12-31'), MAX(price_index) FILTER (WHERE month_end_date=DATE '2025-12-31'), ROUND(100*(MAX(price_index) FILTER (WHERE month_end_date=DATE '2025-12-31')/MAX(price_index) FILTER (WHERE month_end_date=DATE '2020-12-31')-1),1) FROM ref_property_price_index GROUP BY 1 ORDER BY 1"),
    P(3, "Complaints per category by year as a pivot using DuckDB `PIVOT` on `year(received_date)` with counts. Return `category` and one column per year ordered ascending; sorted by `category`. Cast the year to text in a subquery first: `SELECT category, CAST(year(received_date) AS VARCHAR) AS yr FROM complaint`.",
      "SELECT * FROM (PIVOT (SELECT category, CAST(year(received_date) AS VARCHAR) AS yr FROM complaint) ON yr IN ('2018','2019','2020','2021','2022','2023','2024','2025') USING COUNT(*) GROUP BY category) ORDER BY category"),
])
