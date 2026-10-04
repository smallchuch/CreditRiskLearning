SELECT application_id, COALESCE(CAST(broker_id AS VARCHAR), 'No broker') FROM loan_application WHERE application_id <= 12 ORDER BY application_id
