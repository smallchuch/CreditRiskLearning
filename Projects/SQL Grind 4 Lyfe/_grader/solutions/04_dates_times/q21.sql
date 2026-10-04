SELECT DISTINCT snapshot_date, day(last_day(snapshot_date)) AS d, snapshot_date = last_day(snapshot_date) AS me FROM loan_monthly_snapshot WHERE snapshot_date >= DATE '2025-01-01' ORDER BY 1
