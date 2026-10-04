SELECT MIN(original_amount), MAX(original_amount), ROUND(AVG(original_amount),0) FROM loan WHERE loan_status='Active'
