WITH f AS (SELECT primary_customer_id, MIN(application_date) AS d FROM loan_application GROUP BY 1) SELECT year(d), COUNT(*) FROM f GROUP BY 1 ORDER BY 1
