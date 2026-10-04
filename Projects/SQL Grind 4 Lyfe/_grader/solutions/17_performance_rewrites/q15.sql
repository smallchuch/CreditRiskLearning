SELECT COUNT(*) FROM (SELECT loan_id FROM loan_monthly_snapshot GROUP BY 1 HAVING MAX(days_past_due)>=30)
