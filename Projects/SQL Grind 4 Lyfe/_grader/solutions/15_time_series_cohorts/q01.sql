SELECT year(origination_date) || '-Q' || quarter(origination_date) AS v, COUNT(*) FROM loan GROUP BY 1 ORDER BY 1
