SELECT loan_id, a, RANK() OVER (ORDER BY a DESC), DENSE_RANK() OVER (ORDER BY a DESC) FROM (SELECT loan_id, ROUND(original_amount,-5) AS a FROM loan WHERE loan_id <= 30) ORDER BY 3, 1
