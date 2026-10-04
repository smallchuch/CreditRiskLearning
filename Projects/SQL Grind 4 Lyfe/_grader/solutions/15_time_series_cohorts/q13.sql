SELECT year(l.fixed_rate_expiry_date) || '-Q' || quarter(l.fixed_rate_expiry_date), COUNT(*), ROUND(SUM(s.closing_balance),0) FROM loan l JOIN loan_monthly_snapshot s ON s.loan_id=l.loan_id AND s.snapshot_date=DATE '2025-12-31'
WHERE l.loan_status='Active' AND l.fixed_rate_expiry_date >= DATE '2026-01-01' AND l.fixed_rate_expiry_date < DATE '2027-01-01' GROUP BY 1 ORDER BY 1
