SELECT ROUND(100.0*COUNT(*) FILTER (WHERE decision IS NULL)/COUNT(*),2) FROM loan_application
