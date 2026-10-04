SELECT month(origination_date), ROUND(COUNT(*)/7.0,1) FROM loan WHERE year(origination_date) BETWEEN 2019 AND 2025 GROUP BY 1 ORDER BY 1
