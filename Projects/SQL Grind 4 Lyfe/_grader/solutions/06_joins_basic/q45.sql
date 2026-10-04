SELECT s.team, COUNT(*) FROM loan l JOIN dim_staff s ON s.staff_id=l.assessor_staff_id WHERE l.origination_date >= DATE '2021-01-01' AND l.origination_date < DATE '2022-01-01' GROUP BY 1 ORDER BY 1
