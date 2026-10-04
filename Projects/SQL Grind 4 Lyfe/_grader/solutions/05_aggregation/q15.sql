SELECT rate_type, loan_status, COUNT(*) AS loans FROM loan GROUP BY ALL ORDER BY 1,2
