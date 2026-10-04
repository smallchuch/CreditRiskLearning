SELECT hardship_type, COUNT(*) AS n, COUNT(*) FILTER (WHERE arrangement_status='Active') FROM hardship_arrangement GROUP BY 1 ORDER BY n DESC, 1
