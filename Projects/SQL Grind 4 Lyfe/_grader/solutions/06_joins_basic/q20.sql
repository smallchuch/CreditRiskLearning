SELECT DISTINCT s.snapshot_date, d.day_name FROM loan_monthly_snapshot s JOIN dim_date d ON d.full_date=s.snapshot_date WHERE s.snapshot_date >= DATE '2025-01-01' ORDER BY 1
