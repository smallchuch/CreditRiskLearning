SELECT l.loan_id, b.firm_name, b.aggregator FROM loan l JOIN dim_broker b ON b.broker_id=l.broker_id WHERE l.channel='Broker' AND l.loan_id <= 200 ORDER BY l.loan_id
