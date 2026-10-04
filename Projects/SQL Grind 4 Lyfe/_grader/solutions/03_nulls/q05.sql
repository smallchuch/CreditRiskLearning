SELECT loan_id, COALESCE(fixed_rate_expiry_date, DATE '9999-12-31') FROM loan WHERE loan_id <= 15 ORDER BY loan_id
