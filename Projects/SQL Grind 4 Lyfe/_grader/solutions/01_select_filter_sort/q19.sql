SELECT loan_id, original_amount FROM loan WHERE channel='Broker' AND loan_status='Active' ORDER BY original_amount DESC, loan_id LIMIT 5
