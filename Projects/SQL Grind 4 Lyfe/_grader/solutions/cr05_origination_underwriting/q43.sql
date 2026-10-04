SELECT year(application_date), ROUND(100.0*COUNT(*) FILTER (WHERE decision='Approved')/COUNT(decision),1) FROM loan_application WHERE channel='Digital' GROUP BY 1 ORDER BY 1
