SELECT b.broker_id, b.firm_name FROM dim_broker b LEFT JOIN loan l ON l.broker_id=b.broker_id WHERE l.loan_id IS NULL ORDER BY 1
