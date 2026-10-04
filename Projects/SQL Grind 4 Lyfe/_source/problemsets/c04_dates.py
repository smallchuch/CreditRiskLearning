from . import P

PRIMER = r"""
## Dates: the four verbs

```
 PICK A PART      year(d)  month(d)  day(d)  dayofweek(d)  quarter(d)  strftime(d,'%Y-%m')
 CHOP / SNAP      date_trunc('month', d)   -> first day of that month
 MOVE             d + INTERVAL 3 MONTH     d - INTERVAL 7 DAY      d + 30   (days)
 MEASURE          date_diff('month', d1, d2)   d2 - d1  (days)   age(d2, d1)
```

```
  date_trunc('month', DATE '2025-03-17')  ->  2025-03-01
  last day of month  =  date_trunc('month', d) + INTERVAL 1 MONTH - INTERVAL 1 DAY
  month-end date     =  last_day(d)
```

### Rules of thumb
* Range filters: `d >= '2025-01-01' AND d < '2026-01-01'` beats `year(d) = 2025` (clean, index-friendly, works with timestamps).
* `date_diff('month', a, b)` counts month **boundaries** crossed, not full months. Decide whether you want that.
* Age = `date_diff('year', dob, ref_date)` is boundary-based too; precise age uses `date_sub('year', dob, ref)`.
* The snapshot date for this bank is **2025-12-31** - use it instead of `CURRENT_DATE` so your answers don't change tomorrow.
"""

CONCEPT = dict(id="04_dates_times", title="04 - Dates: extract, truncate, add, diff", primer=PRIMER, problems=[
    P(1, "How many loans were originated in calendar year 2022? One number.",
      "SELECT COUNT(*) FROM loan WHERE origination_date >= DATE '2022-01-01' AND origination_date < DATE '2023-01-01'"),
    P(1, "Return the earliest and latest `origination_date` on the `loan` table as two columns.",
      "SELECT MIN(origination_date), MAX(origination_date) FROM loan"),
    P(1, "For loans 1-10: `loan_id`, `origination_date`, and the year and month of origination as two integer columns. Sort by `loan_id`.",
      "SELECT loan_id, origination_date, year(origination_date), month(origination_date) FROM loan WHERE loan_id <= 10 ORDER BY loan_id"),
    P(1, "Loans 1-10: `loan_id` and the first day of the month in which each was originated (`date_trunc`). Sort by `loan_id`.",
      "SELECT loan_id, CAST(date_trunc('month', origination_date) AS DATE) FROM loan WHERE loan_id <= 10 ORDER BY loan_id"),
    P(1, "Loans 1-10: `loan_id` and the date exactly 6 months after origination. Sort by `loan_id`.",
      "SELECT loan_id, CAST(origination_date + INTERVAL 6 MONTH AS DATE) FROM loan WHERE loan_id <= 10 ORDER BY loan_id"),
    P(1, "Number of loans originated per calendar year. Return `yr`, `loans`, sorted by `yr`.",
      "SELECT year(origination_date) AS yr, COUNT(*) FROM loan GROUP BY 1 ORDER BY 1"),
    P(2, "Loans originated per month in 2024. Return `month_start` (date), `loans`, sorted by `month_start`.",
      "SELECT CAST(date_trunc('month', origination_date) AS DATE) AS m, COUNT(*) FROM loan WHERE origination_date >= DATE '2024-01-01' AND origination_date < DATE '2025-01-01' GROUP BY 1 ORDER BY 1"),
    P(2, "Months on book as at the snapshot date 2025-12-31 for loans 1-12: `loan_id`, `date_diff('month', origination_date, DATE '2025-12-31')`. Sort by `loan_id`.",
      "SELECT loan_id, date_diff('month', origination_date, DATE '2025-12-31') FROM loan WHERE loan_id <= 12 ORDER BY loan_id"),
    P(2, "Which day of the week do applications get lodged on? Return `dow` (0=Sunday), `applications`, sorted by `dow`.",
      "SELECT dayofweek(application_date) AS dow, COUNT(*) FROM loan_application GROUP BY 1 ORDER BY 1"),
    P(2, "Time to decision: for approved or declined applications (`decision_date` not null) compute the average number of days from `application_date` to `decision_date`, rounded to 1 dp, by `channel`. Return `channel`, `avg_days`; sorted by `channel`.",
      "SELECT channel, ROUND(AVG(decision_date - application_date),1) FROM loan_application WHERE decision_date IS NOT NULL GROUP BY 1 ORDER BY 1"),
    P(2, "Customer age at 2025-12-31 (whole years using `date_diff('year', date_of_birth, DATE '2025-12-31')`) for customers 1-10 with a DOB. Return `customer_id`, `age`, sorted by `customer_id`.",
      "SELECT customer_id, date_diff('year', date_of_birth, DATE '2025-12-31') FROM customer WHERE customer_id <= 10 AND date_of_birth IS NOT NULL ORDER BY customer_id"),
    P(2, "Fixed-rate expiry cliff: how many active loans have a `fixed_rate_expiry_date` in the 90 days AFTER 2025-12-31 (exclusive of the 31st, up to and including 2026-03-31)? One number.",
      "SELECT COUNT(*) FROM loan WHERE loan_status='Active' AND fixed_rate_expiry_date > DATE '2025-12-31' AND fixed_rate_expiry_date <= DATE '2026-03-31'"),
    P(2, "Last day of the month for each `origination_date` of loans 1-8, using `last_day`. Return `loan_id`, `month_end`; sorted by `loan_id`.",
      "SELECT loan_id, last_day(origination_date) FROM loan WHERE loan_id <= 8 ORDER BY loan_id"),
    P(2, "Loans that closed within 12 months of origination (closure date `<= origination_date + INTERVAL 12 MONTH`). Count them by `closure_reason`. Return `closure_reason`, `loans`; sorted by `loans` descending then `closure_reason`.",
      "SELECT closure_reason, COUNT(*) FROM loan WHERE closed_date IS NOT NULL AND closed_date <= origination_date + INTERVAL 12 MONTH GROUP BY 1 ORDER BY 2 DESC, 1"),
    P(2, "Quarterly application volume for 2025 using `quarter()`. Return `q`, `applications`, sorted by `q`.",
      "SELECT quarter(application_date) AS q, COUNT(*) FROM loan_application WHERE application_date >= DATE '2025-01-01' AND application_date < DATE '2026-01-01' GROUP BY 1 ORDER BY 1"),
    P(2, "Australian financial year (July-June). Using `dim_date.fiscal_year`, count loans originated per fiscal year: join loan to dim_date on `full_date = origination_date`. Return `fiscal_year`, `loans`; sorted by `fiscal_year`.",
      "SELECT d.fiscal_year, COUNT(*) FROM loan l JOIN dim_date d ON d.full_date = l.origination_date GROUP BY 1 ORDER BY 1"),
    P(3, "Settlement lag: for settled applications that became loans (join `loan_application` to `loan` on `application_id`), the average days from `application_date` to `origination_date`, rounded to 1 dp, by application `channel`. Return `channel`, `avg_days`; sorted by `channel`.",
      "SELECT a.channel, ROUND(AVG(l.origination_date - a.application_date),1) FROM loan_application a JOIN loan l ON l.application_id = a.application_id GROUP BY 1 ORDER BY 1"),
    P(3, "Loans whose `maturity_date` does not match `origination_date + term_months`. Allow +/- 3 days. Return a count of mismatches (probably 0 - that is a good control test, `empty_ok`).",
      "SELECT COUNT(*) FROM loan WHERE ABS(maturity_date - CAST(origination_date + INTERVAL 1 MONTH * term_months AS DATE)) > 3",
      hint="`origination_date + INTERVAL 1 MONTH * term_months` multiplies an interval by a column."),
    P(3, "Business-day check: how many loans were originated on a day where `dim_date.is_business_day` is false? (Settlements shouldn't happen then.) One number.",
      "SELECT COUNT(*) FROM loan l JOIN dim_date d ON d.full_date = l.origination_date WHERE NOT d.is_business_day"),
    P(3, "Seasoning buckets. For ACTIVE loans compute months on book at 2025-12-31 and bucket into `'0-11'`, `'12-23'`, `'24-59'`, `'60+'`. Return `bucket`, `loans` sorted by the bucket's lower bound (use CASE ordering or a numeric key and drop it, order matters).",
      """SELECT bucket, COUNT(*) FROM (
  SELECT CASE WHEN m < 12 THEN '0-11' WHEN m < 24 THEN '12-23' WHEN m < 60 THEN '24-59' ELSE '60+' END AS bucket,
         CASE WHEN m < 12 THEN 1 WHEN m < 24 THEN 2 WHEN m < 60 THEN 3 ELSE 4 END AS k
  FROM (SELECT date_diff('month', origination_date, DATE '2025-12-31') AS m FROM loan WHERE loan_status='Active')) GROUP BY bucket, k ORDER BY k"""),
    P(3, "Month-end snapshot dates in `loan_monthly_snapshot`: list each distinct `snapshot_date` in 2025 along with the number of calendar days in that month (`day(last_day(snapshot_date))`) and whether it equals the month's last day (`is_month_end`). Return `snapshot_date`, `days_in_month`, `is_month_end`; sorted by `snapshot_date`.",
      "SELECT DISTINCT snapshot_date, day(last_day(snapshot_date)) AS d, snapshot_date = last_day(snapshot_date) AS me FROM loan_monthly_snapshot WHERE snapshot_date >= DATE '2025-01-01' ORDER BY 1"),
    P(3, "Applications decided over a weekend: count approved/declined applications whose `decision_date` falls on Saturday or Sunday (`dim_date.is_weekend`). One number.",
      "SELECT COUNT(*) FROM loan_application a JOIN dim_date d ON d.full_date = a.decision_date WHERE d.is_weekend"),
    P(3, "Event timestamp bucketing. In `application_status_history`, count status events per hour of the day (`hour(status_ts)`). Return `hr`, `events`, sorted by `hr`.",
      "SELECT hour(status_ts) AS hr, COUNT(*) FROM application_status_history GROUP BY 1 ORDER BY 1"),
])
