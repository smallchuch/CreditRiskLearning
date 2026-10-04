SELECT purpose, ROUND(100*SUM(original_amount)/SUM(SUM(original_amount)) OVER (),1) AS s FROM loan GROUP BY 1 ORDER BY s DESC, 1
