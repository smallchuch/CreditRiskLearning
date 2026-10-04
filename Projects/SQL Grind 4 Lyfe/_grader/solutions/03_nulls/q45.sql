SELECT ROUND(100.0*COUNT(*) FILTER (WHERE failure_reason IS NULL)/COUNT(*),2) FROM loan_payment
