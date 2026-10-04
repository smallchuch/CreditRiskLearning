SELECT COUNT(*) FROM loan WHERE loan_status='Active' AND fixed_rate_expiry_date > DATE '2025-12-31' AND fixed_rate_expiry_date <= DATE '2026-03-31'
