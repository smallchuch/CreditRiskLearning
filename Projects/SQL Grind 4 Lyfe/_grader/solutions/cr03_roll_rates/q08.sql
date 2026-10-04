WITH x AS (SELECT loan_id, snapshot_date, months_on_book AS mob, days_past_due AS d, LAG(days_past_due) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS p FROM loan_monthly_snapshot),
ent AS (SELECT loan_id, MIN(mob) AS mob FROM x WHERE snapshot_date>=DATE '2024-01-31' AND snapshot_date<=DATE '2024-12-31' AND d>=30 AND COALESCE(p,0)<30 GROUP BY 1)
SELECT COUNT(*), COUNT(*) FILTER (WHERE c.loan_id IS NOT NULL), ROUND(100.0*COUNT(*) FILTER (WHERE c.loan_id IS NOT NULL)/COUNT(*),1)
FROM ent LEFT JOIN (SELECT DISTINCT e.loan_id FROM ent e JOIN x y ON y.loan_id=e.loan_id AND y.mob BETWEEN e.mob+1 AND e.mob+6 AND y.d=0) c ON c.loan_id=ent.loan_id
