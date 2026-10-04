SELECT loan_id, ROUND(original_amount, -4) FROM loan WHERE loan_id <= 10 ORDER BY loan_id
