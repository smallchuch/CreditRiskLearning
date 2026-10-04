SELECT loan_id, ROUND(original_amount / NULLIF(io_period_months,0),2) FROM loan WHERE loan_id <= 30 ORDER BY loan_id
