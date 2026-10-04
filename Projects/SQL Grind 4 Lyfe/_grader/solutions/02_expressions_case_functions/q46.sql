SELECT loan_id, CEIL(original_amount/50000)*50000 FROM loan WHERE loan_id <= 12 ORDER BY loan_id
