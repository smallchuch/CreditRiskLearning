SELECT loan_id, ROUND(security_value_at_origination*0.8-original_amount,0) FROM loan WHERE loan_id <= 12 ORDER BY loan_id
