SELECT broker_id, firm_name, status, status_change_date FROM dim_broker WHERE status <> 'Active' ORDER BY status_change_date, broker_id
