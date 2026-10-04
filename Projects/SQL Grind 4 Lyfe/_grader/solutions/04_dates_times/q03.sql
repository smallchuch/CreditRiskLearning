SELECT loan_id, origination_date, year(origination_date), month(origination_date) FROM loan WHERE loan_id <= 10 ORDER BY loan_id
