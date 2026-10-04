WITH f AS (SELECT loan_id, MIN(snapshot_date) AS d FROM loan_monthly_snapshot WHERE days_past_due>=30 GROUP BY 1),
c AS (SELECT f.loan_id, f.d, MIN(a.activity_date) AS ca FROM f JOIN collections_activity a ON a.loan_id=f.loan_id AND a.activity_date>=f.d GROUP BY 1,2)
SELECT ROUND(MEDIAN(ca-d),1) FROM c
