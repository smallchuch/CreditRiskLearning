SELECT hardship_flag, COUNT(*), ROUND(SUM(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2024-12-31' AND loan_status<>'Closed' AND days_past_due>=30 GROUP BY 1 ORDER BY 1
