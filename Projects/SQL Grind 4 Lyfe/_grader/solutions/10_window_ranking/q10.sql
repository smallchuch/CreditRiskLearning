SELECT application_id, status FROM application_status_history WHERE application_id <= 15 QUALIFY ROW_NUMBER() OVER (PARTITION BY application_id ORDER BY status_ts DESC, event_id DESC)=1 ORDER BY 1
