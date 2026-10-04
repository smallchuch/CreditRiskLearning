SELECT COUNT(*) FROM (SELECT 1 FROM application_status_history QUALIFY ROW_NUMBER() OVER (PARTITION BY application_id, status ORDER BY loaded_at, event_id)=1)
