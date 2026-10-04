SELECT primary_customer_id, loan_id, origination_date FROM loan QUALIFY ROW_NUMBER() OVER (PARTITION BY primary_customer_id ORDER BY origination_date, loan_id)=2 ORDER BY 1 LIMIT 10
