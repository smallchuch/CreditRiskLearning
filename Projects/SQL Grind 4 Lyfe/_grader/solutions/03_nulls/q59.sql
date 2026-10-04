SELECT loan_id, COALESCE(closed_date, fixed_rate_expiry_date, maturity_date) FROM loan WHERE loan_id<=10 ORDER BY loan_id
