SELECT l.loan_id, l.original_amount, (SELECT ROUND(AVG(i.original_amount),0) FROM loan i WHERE i.purpose=l.purpose) FROM loan l WHERE l.loan_id <= 8 ORDER BY 1
