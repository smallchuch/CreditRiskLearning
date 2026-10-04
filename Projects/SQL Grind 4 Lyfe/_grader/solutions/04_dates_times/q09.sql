SELECT dayofweek(application_date) AS dow, COUNT(*) FROM loan_application GROUP BY 1 ORDER BY 1
