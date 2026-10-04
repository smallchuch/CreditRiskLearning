from ._gen import *
MORE_FOR = '04_dates_times'
PROBLEMS = []
for y in YEARS:
    PROBLEMS.append(P(1, f"Loans originated in each quarter of {y}: `quarter` (1-4), `loans`; sorted by quarter.",
      f"SELECT quarter(origination_date), COUNT(*) FROM loan WHERE {yr('origination_date',y)} GROUP BY 1 ORDER BY 1"))
for y in range(2019,2025):
    PROBLEMS.append(P(2, f"Live loans at {y}-12-31 (snapshot, non-closed) whose `fixed_rate_expiry_date` falls within the following 12 months (after {y}-12-31, up to and including {y+1}-12-31). One number.",
      f"SELECT COUNT(*) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date=DATE '{y}-12-31' AND s.loan_status<>'Closed' AND l.fixed_rate_expiry_date > DATE '{y}-12-31' AND l.fixed_rate_expiry_date <= DATE '{y+1}-12-31'"))
for n in (30,60,90,180,365):
    PROBLEMS.append(P(2, f"Loans originated in the last {n} days up to and including the snapshot date 2025-12-31 (`origination_date > DATE '2025-12-31' - {n}`): count and total amount (0 dp). Return `loans`, `amount`.",
      f"SELECT COUNT(*), ROUND(SUM(original_amount),0) FROM loan WHERE origination_date > DATE '2025-12-31' - {n} AND origination_date <= DATE '2025-12-31'"))
for a,b in [(18,30),(30,40),(40,50),(50,65),(65,120)]:
    PROBLEMS.append(P(2, f"Customers aged {a} to {b-1} inclusive at 2025-12-31 (`date_diff('year', date_of_birth, DATE '2025-12-31')`), ignoring NULL DOB: how many? One number.",
      f"SELECT COUNT(*) FROM customer WHERE date_of_birth IS NOT NULL AND date_diff('year', date_of_birth, DATE '2025-12-31') >= {a} AND date_diff('year', date_of_birth, DATE '2025-12-31') < {b}"))
for y in (2021,2023,2025):
    PROBLEMS.append(P(2, f"Applications lodged in {y} by day name (use `dayname(application_date)`): `day_name`, `applications`; sorted by `day_name`.",
      f"SELECT dayname(application_date), COUNT(*) FROM loan_application WHERE {yr('application_date',y)} GROUP BY 1 ORDER BY 1"))
for y in (2020,2022,2024):
    PROBLEMS.append(P(2, f"Business-day check: using `dim_date`, how many business days (`is_business_day`) and public holidays (`is_public_holiday`) are in {y}? Return `business_days`, `public_holidays`.",
      f"SELECT COUNT(*) FILTER (WHERE is_business_day), COUNT(*) FILTER (WHERE is_public_holiday) FROM dim_date WHERE year={y}"))
for y in (2022,2023,2024,2025):
    PROBLEMS.append(P(3, f"Average age in whole years of loans that closed in {y} - (closed_date minus origination_date) in days / 365.25, 2 dp. Return one number.",
      f"SELECT ROUND(AVG((closed_date-origination_date)/365.25),2) FROM loan WHERE closed_date IS NOT NULL AND {yr('closed_date',y)}"))
PROBLEMS += [
 P(3, "The first Monday of each month of 2025: use `date_trunc('week', ...)`-style logic or `dim_date` (`day_of_week`, `day_of_month <= 7`). Return `full_date` for Mondays with `day_of_month <= 7` in 2025 (`day_name = 'Monday'`); sorted ascending.",
   "SELECT full_date FROM dim_date WHERE year=2025 AND day_name='Monday' AND day_of_month<=7 ORDER BY 1"),
 P(3, "Fiscal quarters: loans originated per Australian fiscal quarter (`dim_date.fiscal_year`, `fiscal_quarter`) for fiscal year 2025. `fiscal_quarter`, `loans`; sorted by quarter.",
   "SELECT d.fiscal_quarter, COUNT(*) FROM loan l JOIN dim_date d ON d.full_date=l.origination_date WHERE d.fiscal_year=2025 GROUP BY 1 ORDER BY 1"),
 P(3, "Age at origination bands: for loans originated in 2024 with a primary customer DOB, count by age band `<30`, `30-44`, `45-59`, `60+` using `date_diff('year', dob, origination_date)`. `band`, `loans`; sorted by band.",
   "SELECT CASE WHEN a<30 THEN '<30' WHEN a<45 THEN '30-44' WHEN a<60 THEN '45-59' ELSE '60+' END AS b, COUNT(*) FROM (SELECT date_diff('year', c.date_of_birth, l.origination_date) AS a FROM loan l JOIN customer c ON c.customer_id=l.primary_customer_id WHERE c.date_of_birth IS NOT NULL AND l.origination_date >= DATE '2024-01-01' AND l.origination_date < DATE '2025-01-01') GROUP BY 1 ORDER BY 1"),
 P(3, "Long-dated: loans whose remaining term at 2025-12-31 is over 25 years: `date_diff('month', DATE '2025-12-31', maturity_date) > 300`, loan_status Active. Count. One number.",
   "SELECT COUNT(*) FROM loan WHERE loan_status='Active' AND date_diff('month', DATE '2025-12-31', maturity_date) > 300"),
]
