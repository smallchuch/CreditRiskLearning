SELECT COUNT(*) FROM loan, (SELECT QUANTILE_CONT(original_amount,0.25) AS q1, QUANTILE_CONT(original_amount,0.75) AS q3 FROM loan) q WHERE original_amount > q.q3 + 1.5*(q.q3-q.q1)
