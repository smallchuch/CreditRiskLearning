SELECT ROUND(100.0*COUNT(*) FILTER (WHERE decline_reason_code IS NULL)/COUNT(*),2) FROM loan_application
