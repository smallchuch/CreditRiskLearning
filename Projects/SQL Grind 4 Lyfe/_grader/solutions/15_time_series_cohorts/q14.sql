SELECT CAST(date_trunc('month', l.io_expiry_date) AS DATE), COUNT(*), ROUND(SUM(s.closing_balance),0) FROM loan l JOIN loan_monthly_snapshot s ON s.loan_id=l.loan_id AND s.snapshot_date=DATE '2025-12-31'
WHERE s.repayment_type='Interest Only' AND l.loan_status='Active' AND l.io_expiry_date >= DATE '2026-01-01' AND l.io_expiry_date < DATE '2027-01-01' GROUP BY 1 ORDER BY 1
