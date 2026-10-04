SELECT loan_id, last_day(origination_date) FROM loan WHERE loan_id <= 8 ORDER BY loan_id
