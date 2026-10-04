SELECT COUNT(*), MIN(d) FROM (SELECT loan_id, MIN(snapshot_date) AS d FROM loan_monthly_snapshot WHERE days_past_due>=30 GROUP BY 1)
