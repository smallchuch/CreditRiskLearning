WITH r AS (SELECT loan_id, MAX(months_on_book) AS mx FROM loan_monthly_snapshot WHERE loan_id <= 5000 GROUP BY 1),
sp AS (SELECT loan_id, unnest(generate_series(0, mx)) AS m FROM r)
SELECT sp.loan_id, sp.m FROM sp LEFT JOIN loan_monthly_snapshot s ON s.loan_id=sp.loan_id AND s.months_on_book=sp.m WHERE s.loan_id IS NULL ORDER BY 1,2
