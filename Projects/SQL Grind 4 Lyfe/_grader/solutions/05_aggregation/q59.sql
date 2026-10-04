SELECT purpose, COUNT(*), ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (),1) FROM loan WHERE channel='Digital' GROUP BY 1 ORDER BY 1
