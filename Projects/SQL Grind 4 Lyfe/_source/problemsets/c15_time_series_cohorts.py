from . import P

PRIMER = r"""
## Time-series patterns every credit analyst uses

**Vintage / cohort analysis** - group loans by when they started, then follow each group as it ages:
```
 vintage (orig. quarter)   MOB 0   MOB 6   MOB 12   MOB 24    <- months on book
 2021-Q1                    0.0%    0.2%    0.6%     1.1%     <- % of loans ever 30+ DPD (cumulative)
 2022-Q1                    0.0%    0.3%    0.9%     --
```
Rows = cohort, columns = age. Lines that fan out upward = deteriorating underwriting.

**Date spine** - a calendar of every period so empty periods still show as 0 (LEFT JOIN onto the spine).

**Point-in-time ("as at") queries** - history tables store changes; "what was true on date X" needs `effective_from <= X AND (effective_to IS NULL OR effective_to > X)`.

**Slowly changing facts** - `loan_rate_history` (rate over time), `property_valuation` (value over time), `application_status_history` (status over time). The *latest* row per key is `ROW_NUMBER() ... = 1` / `QUALIFY`.

**Stock vs flow**: *stock* = a balance at a date (snapshot); *flow* = movement in a period (originations, repayments, write-offs). Balance roll-forward: `opening + originations - repayments - write-offs = closing`.
"""

CONCEPT = dict(id="15_time_series_cohorts", title="15 - Time series, cohorts, vintages, point-in-time history", primer=PRIMER, problems=[
    P(1, "Loans originated per quarter, labelled like `2024-Q3`. Return `vintage`, `loans`; sorted by `vintage`. Use `year(...) || '-Q' || quarter(...)`.",
      "SELECT year(origination_date) || '-Q' || quarter(origination_date) AS v, COUNT(*) FROM loan GROUP BY 1 ORDER BY 1"),
    P(1, "Total non-closed balance by month-end for the last 6 snapshot dates (2025-07-31 to 2025-12-31). Return `snapshot_date`, `balance` (0dp); sorted by date.",
      "SELECT snapshot_date, ROUND(SUM(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date >= DATE '2025-07-31' AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(1, "Number of live (non-closed) loans at each year-end 2019-2025 (snapshot dates 12-31). Return `snapshot_date`, `loans`; sorted by date.",
      "SELECT snapshot_date, COUNT(*) FROM loan_monthly_snapshot WHERE month(snapshot_date)=12 AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(2, "Vintage 30+ DPD curve (point values). For loans originated in 2021, the share of loans (1dp %) that are 30+ DPD at months-on-book 12 (`months_on_book = 12`). Return one number, `pct_30plus_mob12` (denominator = loans with a snapshot at MOB 12, non-closed at that date).",
      """SELECT ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=30)/COUNT(*),1) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE year(l.origination_date)=2021 AND s.months_on_book=12 AND s.loan_status<>'Closed'"""),
    P(2, "Vintage table by origination year (2019-2024) at MOB 12: `yr`, `loans_at_mob12`, `pct_30plus` (2dp). Non-closed at that point. Sorted by `yr`.",
      "SELECT year(l.origination_date), COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=30)/COUNT(*),2) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE year(l.origination_date) BETWEEN 2019 AND 2024 AND s.months_on_book=12 AND s.loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(2, "Prepayment/attrition by vintage: for origination years 2019-2023, the % of loans closed within 24 months of origination (`closed_date <= origination_date + INTERVAL 24 MONTH`). Return `yr`, `loans`, `closed_24m_pct` (1dp); sorted by `yr`.",
      "SELECT year(origination_date), COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE closed_date <= origination_date + INTERVAL 24 MONTH)/COUNT(*),1) FROM loan WHERE year(origination_date) BETWEEN 2019 AND 2023 GROUP BY 1 ORDER BY 1"),
    P(2, "Point-in-time balance: total balance of the portfolio at 2023-06-30 (snapshot) for non-closed loans, and the number of loans. Two numbers: `loans`, `balance` (0dp).",
      "SELECT COUNT(*), ROUND(SUM(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2023-06-30' AND loan_status<>'Closed'"),
    P(2, "Date spine with zeros: for each of the 12 months of 2019 show the number of loans originated (0 if none). Return `month_start`, `loans`; sorted by month. Build the month list with `generate_series` and LEFT JOIN the loans onto it.",
      """WITH sp AS (SELECT CAST(unnest(generate_series(DATE '2019-01-01', DATE '2019-12-01', INTERVAL 1 MONTH)) AS DATE) AS ms)
SELECT sp.ms, COUNT(l.loan_id) FROM sp LEFT JOIN loan l ON l.origination_date >= sp.ms AND l.origination_date < sp.ms + INTERVAL 1 MONTH GROUP BY 1 ORDER BY 1"""),
    P(2, "Rate in force at a date: for loans 1-20, the interest rate from `loan_rate_history` in force on 2020-06-30 (where it already existed). Return `loan_id`, `interest_rate_pct`; sorted by `loan_id`.",
      "SELECT loan_id, interest_rate_pct FROM loan_rate_history WHERE loan_id <= 20 AND effective_from <= DATE '2020-06-30' AND (effective_to IS NULL OR effective_to > DATE '2020-06-30') ORDER BY 1"),
    P(2, "Latest valuation per property (non-zero, <= 2025-12-31): how many properties have a latest valuation above $1,000,000? One number.",
      "SELECT COUNT(*) FROM (SELECT property_id, valuation_amount FROM property_valuation WHERE valuation_amount>0 AND valuation_date <= DATE '2025-12-31' QUALIFY ROW_NUMBER() OVER (PARTITION BY property_id ORDER BY valuation_date DESC, valuation_id DESC)=1) WHERE valuation_amount > 1000000"),
    P(3, "Balance roll-forward for Dec 2025 (non-internal loans, all loans): opening balance (snapshot 2025-11-30, non-closed), + new loans originated in Dec (`original_amount`), - closing balance at 2025-12-31 (non-closed). Report `opening`, `originations`, `closing`, and `implied_runoff` = opening + originations - closing (all 0dp). One row.",
      """SELECT ROUND(o,0), ROUND(n,0), ROUND(c,0), ROUND(o+n-c,0) FROM (SELECT
 (SELECT SUM(closing_balance) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-11-30' AND loan_status<>'Closed') AS o,
 (SELECT SUM(original_amount) FROM loan WHERE origination_date >= DATE '2025-12-01' AND origination_date <= DATE '2025-12-31') AS n,
 (SELECT SUM(closing_balance) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed') AS c)"""),
    P(3, "Cumulative ever-30+ by vintage. For loans originated in 2022, compute at MOB 6, 12, 18, 24 the % of loans that have EVER been 30+ DPD up to that MOB (`MAX(days_past_due)>=30` among snapshots with `months_on_book <= k`). Return `mob`, `loans`, `ever_30plus_pct` (2dp) for k in (6,12,18,24); sorted by `mob`. Loans = those 2022 loans that have a snapshot at that MOB.",
      """WITH k AS (SELECT unnest([6,12,18,24]) AS mob)
SELECT k.mob, COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE e.mx>=30)/COUNT(*),2) FROM k JOIN (
  SELECT l.loan_id, s.months_on_book AS mob, MAX(s2.days_past_due) AS mx FROM loan l
  JOIN loan_monthly_snapshot s ON s.loan_id=l.loan_id JOIN loan_monthly_snapshot s2 ON s2.loan_id=l.loan_id AND s2.months_on_book<=s.months_on_book
  WHERE year(l.origination_date)=2022 AND s.months_on_book IN (6,12,18,24) GROUP BY 1,2) e ON e.mob=k.mob GROUP BY k.mob ORDER BY k.mob"""),
    P(3, "Fixed-rate expiry wall. Active loans with fixed expiry dates after the snapshot: balance maturing per quarter. Return `quarter` (label `YYYY-Qn`), `loans`, `balance` (0dp, snapshot 2025-12-31) for fixed expiry dates in 2026; sorted by quarter. Join `loan` and the snapshot.",
      """SELECT year(l.fixed_rate_expiry_date) || '-Q' || quarter(l.fixed_rate_expiry_date), COUNT(*), ROUND(SUM(s.closing_balance),0) FROM loan l JOIN loan_monthly_snapshot s ON s.loan_id=l.loan_id AND s.snapshot_date=DATE '2025-12-31'
WHERE l.loan_status='Active' AND l.fixed_rate_expiry_date >= DATE '2026-01-01' AND l.fixed_rate_expiry_date < DATE '2027-01-01' GROUP BY 1 ORDER BY 1"""),
    P(3, "IO cliff: Active interest-only loans (snapshot `repayment_type='Interest Only'` at 2025-12-31) with `io_expiry_date` in 2026, by month. Return `io_month` (first day of the month, date), `loans`, `balance` (0dp); sorted by `io_month`.",
      """SELECT CAST(date_trunc('month', l.io_expiry_date) AS DATE), COUNT(*), ROUND(SUM(s.closing_balance),0) FROM loan l JOIN loan_monthly_snapshot s ON s.loan_id=l.loan_id AND s.snapshot_date=DATE '2025-12-31'
WHERE s.repayment_type='Interest Only' AND l.loan_status='Active' AND l.io_expiry_date >= DATE '2026-01-01' AND l.io_expiry_date < DATE '2027-01-01' GROUP BY 1 ORDER BY 1"""),
    P(3, "Status history as-at: the status of each application as at 2024-06-30 (last event with `status_ts <= '2024-06-30 23:59:59'`, using the latest event by ts then event_id) for applications lodged between 2024-06-01 and 2024-06-15. Count by `status`. Return `status`, `apps`; sorted by `apps` descending then `status`.",
      """SELECT status, COUNT(*) AS n FROM (SELECT h.application_id, h.status FROM application_status_history h JOIN loan_application a USING (application_id) WHERE a.application_date BETWEEN DATE '2024-06-01' AND DATE '2024-06-15' AND h.status_ts <= TIMESTAMP '2024-06-30 23:59:59'
QUALIFY ROW_NUMBER() OVER (PARTITION BY h.application_id ORDER BY h.status_ts DESC, h.event_id DESC)=1) GROUP BY 1 ORDER BY n DESC, 1"""),
    P(3, "Time-to-event: for settled applications, days from 'Submitted' to 'Settled' in `application_status_history` (min `status_ts` per status). Return the median days (1 dp) overall as `median_days`. One number. (Use MIN per application for each status to ignore duplicates.)",
      """WITH s AS (SELECT application_id, MIN(status_ts) FILTER (WHERE status='Submitted') AS a, MIN(status_ts) FILTER (WHERE status='Settled') AS b FROM application_status_history GROUP BY 1)
SELECT ROUND(MEDIAN(date_diff('second', a, b)/86400.0),1) FROM s WHERE a IS NOT NULL AND b IS NOT NULL"""),
    P(3, "Seasonality: average loans originated per calendar month number across 2019-2025 (sum of loans by month number / 7 years, 1dp). Return `month_no`, `avg_loans`; sorted by month. (2018 and partial year excluded.)",
      "SELECT month(origination_date), ROUND(COUNT(*)/7.0,1) FROM loan WHERE year(origination_date) BETWEEN 2019 AND 2025 GROUP BY 1 ORDER BY 1"),
    P(3, "Moving 12-month default flow: for each month-end snapshot in 2025, count loans that are 90+ DPD this month but were NOT 90+ last month (`new_90plus`). Return `snapshot_date`, `new_90plus`; sorted by date. (Non-closed.)",
      """SELECT snapshot_date, COUNT(*) FILTER (WHERE days_past_due>=90 AND COALESCE(p,0)<90) FROM (SELECT snapshot_date, days_past_due, loan_status, LAG(days_past_due) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS p FROM loan_monthly_snapshot)
WHERE snapshot_date >= DATE '2025-01-01' AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1"""),
    P(3, "Customer tenure vs product: average years between `customer_since` and the customer's first loan origination, per customer `segment` (2dp). Return `segment`, `avg_years`; sorted by segment. (Use `date_diff('day', ...)/365.25`; first loan = MIN origination per primary customer; ignore negatives.)",
      """SELECT c.segment, ROUND(AVG(date_diff('day', c.customer_since, f.d)/365.25),2) FROM customer c JOIN (SELECT primary_customer_id, MIN(origination_date) AS d FROM loan GROUP BY 1) f ON f.primary_customer_id=c.customer_id WHERE f.d >= c.customer_since GROUP BY 1 ORDER BY 1"""),
])
