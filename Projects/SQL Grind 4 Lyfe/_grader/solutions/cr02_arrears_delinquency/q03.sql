SELECT ROUND(SUM(arrears_amount),0), COUNT(*) FILTER (WHERE arrears_amount>0) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'
