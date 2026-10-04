SELECT loan_id, CAST(origination_date + INTERVAL 6 MONTH AS DATE) FROM loan WHERE loan_id <= 10 ORDER BY loan_id
