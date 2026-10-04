SELECT MAX(original_amount) FROM loan WHERE original_amount < (SELECT MAX(original_amount) FROM loan)
