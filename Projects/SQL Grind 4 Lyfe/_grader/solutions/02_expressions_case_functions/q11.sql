SELECT LOWER(SPLIT_PART(email, '@', 2)) AS domain, COUNT(*) AS customers FROM customer GROUP BY 1 ORDER BY 2 DESC, 1
