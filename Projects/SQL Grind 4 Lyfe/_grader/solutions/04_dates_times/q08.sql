SELECT loan_id, date_diff('month', origination_date, DATE '2025-12-31') FROM loan WHERE loan_id <= 12 ORDER BY loan_id
