SELECT COUNT(*) FROM loan o WHERE original_amount > (SELECT AVG(original_amount) FROM loan i WHERE i.purpose=o.purpose)
