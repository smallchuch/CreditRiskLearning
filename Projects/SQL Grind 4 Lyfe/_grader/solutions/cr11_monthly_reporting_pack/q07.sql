WITH b AS (SELECT snapshot_date AS d, SUM(closing_balance) AS bal FROM loan_monthly_snapshot WHERE loan_status<>'Closed' GROUP BY 1),
n AS (SELECT last_day(origination_date) AS d, SUM(original_amount) AS n FROM loan GROUP BY 1)
SELECT d, ROUND(op,0), ROUND(n,0), ROUND(bal,0), ROUND(bal-op-n,0) FROM (SELECT b.d, LAG(b.bal) OVER (ORDER BY b.d) AS op, n.n, b.bal FROM b LEFT JOIN n ON n.d=b.d) WHERE d>=DATE '2025-02-01' ORDER BY d
