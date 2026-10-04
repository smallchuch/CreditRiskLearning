SELECT COUNT(*) FROM loan_application a WHERE NOT EXISTS (SELECT 1 FROM dim_broker b WHERE b.broker_id = a.broker_id AND b.status='Terminated')
