SELECT COUNT(*) FROM (SELECT rate_history_id FROM loan_rate_history GROUP BY 1 HAVING COUNT(*)>1)
