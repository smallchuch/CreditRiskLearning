SELECT s.team, COUNT(*) AS n FROM loan l JOIN dim_staff s ON s.staff_id=l.assessor_staff_id GROUP BY 1 ORDER BY n DESC, 1
