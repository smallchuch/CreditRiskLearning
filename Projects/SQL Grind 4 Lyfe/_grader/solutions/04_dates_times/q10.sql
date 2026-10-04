SELECT channel, ROUND(AVG(decision_date - application_date),1) FROM loan_application WHERE decision_date IS NOT NULL GROUP BY 1 ORDER BY 1
