# 04 - Dates: extract, truncate, add, diff

`answers/04_dates_times/qNN.sql` &nbsp;|&nbsp; check with: `grade 04` or `grade 04 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

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

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

How many loans were originated in calendar year 2022? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Return the earliest and latest `origination_date` on the `loan` table as two columns.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q03 &nbsp; ★ &nbsp; (warm-up)

For loans 1-10: `loan_id`, `origination_date`, and the year and month of origination as two integer columns. Sort by `loan_id`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★ &nbsp; (warm-up)

Loans 1-10: `loan_id` and the first day of the month in which each was originated (`date_trunc`). Sort by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★ &nbsp; (warm-up)

Loans 1-10: `loan_id` and the date exactly 6 months after origination. Sort by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★ &nbsp; (warm-up)

Number of loans originated per calendar year. Return `yr`, `loans`, sorted by `yr`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

Loans originated per month in 2024. Return `month_start` (date), `loans`, sorted by `month_start`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

Months on book as at the snapshot date 2025-12-31 for loans 1-12: `loan_id`, `date_diff('month', origination_date, DATE '2025-12-31')`. Sort by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

Which day of the week do applications get lodged on? Return `dow` (0=Sunday), `applications`, sorted by `dow`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★ &nbsp; (core)

Time to decision: for approved or declined applications (`decision_date` not null) compute the average number of days from `application_date` to `decision_date`, rounded to 1 dp, by `channel`. Return `channel`, `avg_days`; sorted by `channel`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★ &nbsp; (core)

Customer age at 2025-12-31 (whole years using `date_diff('year', date_of_birth, DATE '2025-12-31')`) for customers 1-10 with a DOB. Return `customer_id`, `age`, sorted by `customer_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **9 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★ &nbsp; (core)

Fixed-rate expiry cliff: how many active loans have a `fixed_rate_expiry_date` in the 90 days AFTER 2025-12-31 (exclusive of the 31st, up to and including 2026-03-31)? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q13 &nbsp; ★★ &nbsp; (core)

Last day of the month for each `origination_date` of loans 1-8, using `last_day`. Return `loan_id`, `month_end`; sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q14 &nbsp; ★★ &nbsp; (core)

Loans that closed within 12 months of origination (closure date `<= origination_date + INTERVAL 12 MONTH`). Count them by `closure_reason`. Return `closure_reason`, `loans`; sorted by `loans` descending then `closure_reason`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★ &nbsp; (core)

Quarterly application volume for 2025 using `quarter()`. Return `q`, `applications`, sorted by `q`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★ &nbsp; (core)

Australian financial year (July-June). Using `dim_date.fiscal_year`, count loans originated per fiscal year: join loan to dim_date on `full_date = origination_date`. Return `fiscal_year`, `loans`; sorted by `fiscal_year`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q17 &nbsp; ★★★ &nbsp; (challenge)

Settlement lag: for settled applications that became loans (join `loan_application` to `loan` on `application_id`), the average days from `application_date` to `origination_date`, rounded to 1 dp, by application `channel`. Return `channel`, `avg_days`; sorted by `channel`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q18 &nbsp; ★★★ &nbsp; (challenge)

Loans whose `maturity_date` does not match `origination_date + term_months`. Allow +/- 3 days. Return a count of mismatches (probably 0 - that is a good control test, `empty_ok`).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

<details><summary>hint</summary>

`origination_date + INTERVAL 1 MONTH * term_months` multiplies an interval by a column.

</details>

### Q19 &nbsp; ★★★ &nbsp; (challenge)

Business-day check: how many loans were originated on a day where `dim_date.is_business_day` is false? (Settlements shouldn't happen then.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★★★ &nbsp; (challenge)

Seasoning buckets. For ACTIVE loans compute months on book at 2025-12-31 and bucket into `'0-11'`, `'12-23'`, `'24-59'`, `'60+'`. Return `bucket`, `loans` sorted by the bucket's lower bound (use CASE ordering or a numeric key and drop it, order matters).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q21 &nbsp; ★★★ &nbsp; (challenge)

Month-end snapshot dates in `loan_monthly_snapshot`: list each distinct `snapshot_date` in 2025 along with the number of calendar days in that month (`day(last_day(snapshot_date))`) and whether it equals the month's last day (`is_month_end`). Return `snapshot_date`, `days_in_month`, `is_month_end`; sorted by `snapshot_date`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q22 &nbsp; ★★★ &nbsp; (challenge)

Applications decided over a weekend: count approved/declined applications whose `decision_date` falls on Saturday or Sunday (`dim_date.is_weekend`). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★★ &nbsp; (challenge)

Event timestamp bucketing. In `application_status_history`, count status events per hour of the day (`hour(status_ts)`). Return `hr`, `events`, sorted by `hr`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **24 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q24 &nbsp; ★ &nbsp; (warm-up)

Loans originated in each quarter of 2019: `quarter` (1-4), `loans`; sorted by quarter.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q25 &nbsp; ★ &nbsp; (warm-up)

Loans originated in each quarter of 2020: `quarter` (1-4), `loans`; sorted by quarter.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q26 &nbsp; ★ &nbsp; (warm-up)

Loans originated in each quarter of 2021: `quarter` (1-4), `loans`; sorted by quarter.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q27 &nbsp; ★ &nbsp; (warm-up)

Loans originated in each quarter of 2022: `quarter` (1-4), `loans`; sorted by quarter.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q28 &nbsp; ★ &nbsp; (warm-up)

Loans originated in each quarter of 2023: `quarter` (1-4), `loans`; sorted by quarter.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q29 &nbsp; ★ &nbsp; (warm-up)

Loans originated in each quarter of 2024: `quarter` (1-4), `loans`; sorted by quarter.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q30 &nbsp; ★ &nbsp; (warm-up)

Loans originated in each quarter of 2025: `quarter` (1-4), `loans`; sorted by quarter.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q31 &nbsp; ★★ &nbsp; (core)

Live loans at 2019-12-31 (snapshot, non-closed) whose `fixed_rate_expiry_date` falls within the following 12 months (after 2019-12-31, up to and including 2020-12-31). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q32 &nbsp; ★★ &nbsp; (core)

Live loans at 2020-12-31 (snapshot, non-closed) whose `fixed_rate_expiry_date` falls within the following 12 months (after 2020-12-31, up to and including 2021-12-31). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q33 &nbsp; ★★ &nbsp; (core)

Live loans at 2021-12-31 (snapshot, non-closed) whose `fixed_rate_expiry_date` falls within the following 12 months (after 2021-12-31, up to and including 2022-12-31). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q34 &nbsp; ★★ &nbsp; (core)

Live loans at 2022-12-31 (snapshot, non-closed) whose `fixed_rate_expiry_date` falls within the following 12 months (after 2022-12-31, up to and including 2023-12-31). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q35 &nbsp; ★★ &nbsp; (core)

Live loans at 2023-12-31 (snapshot, non-closed) whose `fixed_rate_expiry_date` falls within the following 12 months (after 2023-12-31, up to and including 2024-12-31). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q36 &nbsp; ★★ &nbsp; (core)

Live loans at 2024-12-31 (snapshot, non-closed) whose `fixed_rate_expiry_date` falls within the following 12 months (after 2024-12-31, up to and including 2025-12-31). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q37 &nbsp; ★★ &nbsp; (core)

Loans originated in the last 30 days up to and including the snapshot date 2025-12-31 (`origination_date > DATE '2025-12-31' - 30`): count and total amount (0 dp). Return `loans`, `amount`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q38 &nbsp; ★★ &nbsp; (core)

Loans originated in the last 60 days up to and including the snapshot date 2025-12-31 (`origination_date > DATE '2025-12-31' - 60`): count and total amount (0 dp). Return `loans`, `amount`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q39 &nbsp; ★★ &nbsp; (core)

Loans originated in the last 90 days up to and including the snapshot date 2025-12-31 (`origination_date > DATE '2025-12-31' - 90`): count and total amount (0 dp). Return `loans`, `amount`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q40 &nbsp; ★★ &nbsp; (core)

Loans originated in the last 180 days up to and including the snapshot date 2025-12-31 (`origination_date > DATE '2025-12-31' - 180`): count and total amount (0 dp). Return `loans`, `amount`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q41 &nbsp; ★★ &nbsp; (core)

Loans originated in the last 365 days up to and including the snapshot date 2025-12-31 (`origination_date > DATE '2025-12-31' - 365`): count and total amount (0 dp). Return `loans`, `amount`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q42 &nbsp; ★★ &nbsp; (core)

Customers aged 18 to 29 inclusive at 2025-12-31 (`date_diff('year', date_of_birth, DATE '2025-12-31')`), ignoring NULL DOB: how many? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q43 &nbsp; ★★ &nbsp; (core)

Customers aged 30 to 39 inclusive at 2025-12-31 (`date_diff('year', date_of_birth, DATE '2025-12-31')`), ignoring NULL DOB: how many? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q44 &nbsp; ★★ &nbsp; (core)

Customers aged 40 to 49 inclusive at 2025-12-31 (`date_diff('year', date_of_birth, DATE '2025-12-31')`), ignoring NULL DOB: how many? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q45 &nbsp; ★★ &nbsp; (core)

Customers aged 50 to 64 inclusive at 2025-12-31 (`date_diff('year', date_of_birth, DATE '2025-12-31')`), ignoring NULL DOB: how many? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q46 &nbsp; ★★ &nbsp; (core)

Customers aged 65 to 119 inclusive at 2025-12-31 (`date_diff('year', date_of_birth, DATE '2025-12-31')`), ignoring NULL DOB: how many? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q47 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2021 by day name (use `dayname(application_date)`): `day_name`, `applications`; sorted by `day_name`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q48 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2023 by day name (use `dayname(application_date)`): `day_name`, `applications`; sorted by `day_name`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q49 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2025 by day name (use `dayname(application_date)`): `day_name`, `applications`; sorted by `day_name`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q50 &nbsp; ★★ &nbsp; (core)

Business-day check: using `dim_date`, how many business days (`is_business_day`) and public holidays (`is_public_holiday`) are in 2020? Return `business_days`, `public_holidays`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q51 &nbsp; ★★ &nbsp; (core)

Business-day check: using `dim_date`, how many business days (`is_business_day`) and public holidays (`is_public_holiday`) are in 2022? Return `business_days`, `public_holidays`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q52 &nbsp; ★★ &nbsp; (core)

Business-day check: using `dim_date`, how many business days (`is_business_day`) and public holidays (`is_public_holiday`) are in 2024? Return `business_days`, `public_holidays`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q53 &nbsp; ★★★ &nbsp; (challenge)

Average age in whole years of loans that closed in 2022 - (closed_date minus origination_date) in days / 365.25, 2 dp. Return one number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q54 &nbsp; ★★★ &nbsp; (challenge)

Average age in whole years of loans that closed in 2023 - (closed_date minus origination_date) in days / 365.25, 2 dp. Return one number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q55 &nbsp; ★★★ &nbsp; (challenge)

Average age in whole years of loans that closed in 2024 - (closed_date minus origination_date) in days / 365.25, 2 dp. Return one number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q56 &nbsp; ★★★ &nbsp; (challenge)

Average age in whole years of loans that closed in 2025 - (closed_date minus origination_date) in days / 365.25, 2 dp. Return one number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q57 &nbsp; ★★★ &nbsp; (challenge)

The first Monday of each month of 2025: use `date_trunc('week', ...)`-style logic or `dim_date` (`day_of_week`, `day_of_month <= 7`). Return `full_date` for Mondays with `day_of_month <= 7` in 2025 (`day_name = 'Monday'`); sorted ascending.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q58 &nbsp; ★★★ &nbsp; (challenge)

Fiscal quarters: loans originated per Australian fiscal quarter (`dim_date.fiscal_year`, `fiscal_quarter`) for fiscal year 2025. `fiscal_quarter`, `loans`; sorted by quarter.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q59 &nbsp; ★★★ &nbsp; (challenge)

Age at origination bands: for loans originated in 2024 with a primary customer DOB, count by age band `<30`, `30-44`, `45-59`, `60+` using `date_diff('year', dob, origination_date)`. `band`, `loans`; sorted by band.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q60 &nbsp; ★★★ &nbsp; (challenge)

Long-dated: loans whose remaining term at 2025-12-31 is over 25 years: `date_diff('month', DATE '2025-12-31', maturity_date) > 300`, loan_status Active. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.
