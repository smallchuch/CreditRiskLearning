SELECT COUNT(*) FROM (SELECT 1 FROM application_status_history GROUP BY application_id, status HAVING COUNT(*)>1)
