WITH x AS (SELECT application_id, COUNT(*) FILTER (WHERE status='Settled') AS s, COUNT(*) FILTER (WHERE status='Submitted') AS sub FROM application_status_history GROUP BY 1)
SELECT COUNT(*) FROM x WHERE s=1 AND sub>1
