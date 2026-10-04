SELECT ROUND(100.0*COUNT(*) FILTER (WHERE withdrawn_date IS NULL)/COUNT(*),2) FROM loan_application
