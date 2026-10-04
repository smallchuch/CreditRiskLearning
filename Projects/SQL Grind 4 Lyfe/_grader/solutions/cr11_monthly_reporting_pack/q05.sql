WITH n AS (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS m, COUNT(*) AS n FROM loan GROUP BY 1),
c AS (SELECT CAST(date_trunc('month', closed_date) AS DATE) AS m, COUNT(*) AS c FROM loan WHERE closed_date IS NOT NULL GROUP BY 1),
l AS (SELECT CAST(date_trunc('month', snapshot_date) AS DATE) AS m, COUNT(*) AS live FROM loan_monthly_snapshot WHERE loan_status<>'Closed' GROUP BY 1),
j AS (SELECT l.m, n.n, c.c, l.live, LAG(l.live) OVER (ORDER BY l.m) AS pl FROM l JOIN n USING (m) LEFT JOIN c USING (m))
SELECT m, n, COALESCE(c,0), n-COALESCE(c,0), live-pl FROM j WHERE m>=DATE '2025-02-01' ORDER BY m
