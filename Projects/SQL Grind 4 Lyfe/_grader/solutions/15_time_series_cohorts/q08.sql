WITH sp AS (SELECT CAST(unnest(generate_series(DATE '2019-01-01', DATE '2019-12-01', INTERVAL 1 MONTH)) AS DATE) AS ms)
SELECT sp.ms, COUNT(l.loan_id) FROM sp LEFT JOIN loan l ON l.origination_date >= sp.ms AND l.origination_date < sp.ms + INTERVAL 1 MONTH GROUP BY 1 ORDER BY 1
