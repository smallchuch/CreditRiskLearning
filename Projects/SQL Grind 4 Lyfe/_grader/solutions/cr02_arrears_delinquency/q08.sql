SELECT hardship_flag, COUNT(*) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed' AND days_past_due>=30 GROUP BY 1 ORDER BY 1
