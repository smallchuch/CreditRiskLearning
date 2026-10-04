SELECT channel, COUNT(*) FILTER (WHERE loan_status='Active'), COUNT(*) FILTER (WHERE loan_status='Closed'), COUNT(*) FILTER (WHERE loan_status='In Recovery') FROM loan GROUP BY 1 ORDER BY 1
