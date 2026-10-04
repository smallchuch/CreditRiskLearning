SELECT loan_id, original_amount, ROUND(original_amount*interest_rate_at_origination_pct/100,2) FROM loan WHERE purpose='Refinance' ORDER BY original_amount DESC, loan_id LIMIT 8
