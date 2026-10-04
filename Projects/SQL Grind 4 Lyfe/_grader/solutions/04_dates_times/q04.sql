SELECT loan_id, CAST(date_trunc('month', origination_date) AS DATE) FROM loan WHERE loan_id <= 10 ORDER BY loan_id
