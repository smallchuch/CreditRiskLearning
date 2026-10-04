SELECT COUNT(*) FROM (SELECT event_id FROM application_status_history GROUP BY 1 HAVING COUNT(*)>1)
