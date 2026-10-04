SELECT purpose, COUNT(*) AS n FROM (SELECT purpose, ROW_NUMBER() OVER (PARTITION BY primary_customer_id ORDER BY origination_date, loan_id) AS rn FROM loan) WHERE rn=1 GROUP BY 1 ORDER BY n DESC, 1
