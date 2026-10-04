SELECT activity_type, COUNT(*) AS n FROM collections_activity GROUP BY 1 ORDER BY n DESC, 1
