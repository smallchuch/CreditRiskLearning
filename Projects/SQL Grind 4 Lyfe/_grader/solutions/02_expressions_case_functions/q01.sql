SELECT loan_id, ROUND(original_amount / term_months, 2) FROM loan WHERE loan_id <= 10 ORDER BY loan_id
