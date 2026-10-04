SELECT loan_id, GREATEST(original_amount, security_value_at_origination*0.5), LEAST(original_amount,600000) FROM loan WHERE loan_id<=12 ORDER BY loan_id
