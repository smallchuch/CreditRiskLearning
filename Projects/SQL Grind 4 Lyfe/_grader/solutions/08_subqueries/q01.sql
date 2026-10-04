SELECT COUNT(*) FROM loan WHERE original_amount > (SELECT AVG(original_amount) FROM loan)
