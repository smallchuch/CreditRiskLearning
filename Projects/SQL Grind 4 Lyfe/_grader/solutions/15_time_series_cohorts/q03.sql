SELECT snapshot_date, COUNT(*) FROM loan_monthly_snapshot WHERE month(snapshot_date)=12 AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1
