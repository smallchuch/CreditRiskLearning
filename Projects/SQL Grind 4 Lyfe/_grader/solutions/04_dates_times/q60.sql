SELECT COUNT(*) FROM loan WHERE loan_status='Active' AND date_diff('month', DATE '2025-12-31', maturity_date) > 300
