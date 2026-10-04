SELECT activity_type, COUNT(*) FILTER (WHERE outcome='Promise to pay'), COUNT(*) FILTER (WHERE outcome='Payment taken'), COUNT(*) AS t FROM collections_activity GROUP BY 1 ORDER BY t DESC, 1
