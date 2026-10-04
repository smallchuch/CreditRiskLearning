WITH sp AS (SELECT CAST(unnest(generate_series(DATE '2025-01-01', DATE '2025-12-01', INTERVAL 1 MONTH)) AS DATE) AS ms)
SELECT last_day(sp.ms), COUNT(l.loan_id) FROM sp LEFT JOIN loan l ON l.origination_date >= sp.ms AND l.origination_date < sp.ms + INTERVAL 1 MONTH GROUP BY sp.ms ORDER BY sp.ms
