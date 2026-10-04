WITH s AS (SELECT application_id, MIN(status_ts) FILTER (WHERE status='Submitted') AS a, MIN(status_ts) FILTER (WHERE status='Settled') AS b FROM application_status_history GROUP BY 1)
SELECT ROUND(MEDIAN(date_diff('second', a, b)/86400.0),1) FROM s WHERE a IS NOT NULL AND b IS NOT NULL
