SELECT application_id, application_date FROM loan_application WHERE channel='Broker' AND broker_id IS NULL ORDER BY application_id
