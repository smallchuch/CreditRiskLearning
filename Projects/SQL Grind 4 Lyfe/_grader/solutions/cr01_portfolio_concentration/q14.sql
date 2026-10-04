WITH y AS (SELECT snapshot_date, SUM(closing_balance) AS b FROM loan_monthly_snapshot WHERE month(snapshot_date)=12 AND loan_status<>'Closed' GROUP BY 1)
SELECT snapshot_date, ROUND(b,0), ROUND(100*(b/LAG(b) OVER (ORDER BY snapshot_date)-1),1) FROM y ORDER BY 1
