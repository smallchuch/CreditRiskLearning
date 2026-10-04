SELECT snapshot_date, days_past_due, LEAD(days_past_due) OVER (ORDER BY snapshot_date) FROM loan_monthly_snapshot WHERE loan_id=1 ORDER BY snapshot_date
