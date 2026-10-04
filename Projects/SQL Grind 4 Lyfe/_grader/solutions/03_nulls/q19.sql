SELECT loan_id, fixed_rate_expiry_date FROM loan WHERE fixed_rate_expiry_date IS NOT NULL ORDER BY fixed_rate_expiry_date, loan_id LIMIT 10
