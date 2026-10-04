CREATE OR REPLACE TABLE scratch.cal AS SELECT CAST(last_day(unnest(generate_series(DATE '2025-01-01', DATE '2025-12-01', INTERVAL 1 MONTH))) AS DATE) AS month_end;
CREATE OR REPLACE TABLE scratch.monthly_loans AS SELECT c.month_end, COUNT(l.loan_id) AS loans FROM scratch.cal c LEFT JOIN loan l ON last_day(l.origination_date)=c.month_end GROUP BY 1;
SELECT month_end, loans FROM scratch.monthly_loans ORDER BY 1
