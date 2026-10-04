SELECT a.channel, ROUND(AVG(l.origination_date - a.application_date),1) FROM loan_application a JOIN loan l ON l.application_id = a.application_id GROUP BY 1 ORDER BY 1
