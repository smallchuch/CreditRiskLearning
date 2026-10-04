SELECT quarter(origination_date), COUNT(*) FROM loan WHERE origination_date >= DATE '2019-01-01' AND origination_date < DATE '2020-01-01' GROUP BY 1 ORDER BY 1
