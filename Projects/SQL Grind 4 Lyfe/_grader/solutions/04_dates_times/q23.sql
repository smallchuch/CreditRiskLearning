SELECT hour(status_ts) AS hr, COUNT(*) FROM application_status_history GROUP BY 1 ORDER BY 1
