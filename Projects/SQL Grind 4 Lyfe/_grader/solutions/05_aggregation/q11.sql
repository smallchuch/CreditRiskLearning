SELECT channel, ROUND(100.0*COUNT(*) FILTER (WHERE decision='Approved')/COUNT(decision),1) FROM loan_application GROUP BY 1 ORDER BY 1
