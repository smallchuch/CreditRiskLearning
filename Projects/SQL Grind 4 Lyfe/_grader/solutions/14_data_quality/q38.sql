SELECT COUNT(*) FROM (SELECT activity_id FROM collections_activity GROUP BY 1 HAVING COUNT(*)>1)
