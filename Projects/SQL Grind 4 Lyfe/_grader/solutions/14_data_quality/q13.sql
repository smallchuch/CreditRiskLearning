SELECT COUNT(*) FILTER (WHERE broker_id IS NULL), ROUND(100.0*COUNT(*) FILTER (WHERE broker_id IS NULL)/COUNT(*),2) FROM loan_application WHERE channel='Broker'
