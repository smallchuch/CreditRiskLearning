SELECT purpose, loan_id, original_amount FROM loan QUALIFY ROW_NUMBER() OVER (PARTITION BY purpose ORDER BY original_amount DESC, loan_id)=2 ORDER BY 1
