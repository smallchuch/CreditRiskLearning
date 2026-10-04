SELECT COUNT(*) FROM loan_monthly_snapshot s WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' AND s.days_past_due=0
AND EXISTS (SELECT 1 FROM loan_monthly_snapshot h WHERE h.loan_id=s.loan_id AND h.days_past_due>=90)
