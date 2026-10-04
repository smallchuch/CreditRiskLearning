SELECT COUNT(*) FROM loan WHERE original_amount >= (SELECT QUANTILE_CONT(original_amount,0.75) FROM loan)
