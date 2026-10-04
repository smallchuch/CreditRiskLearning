SELECT bucket, COUNT(*) FROM (
  SELECT CASE WHEN m < 12 THEN '0-11' WHEN m < 24 THEN '12-23' WHEN m < 60 THEN '24-59' ELSE '60+' END AS bucket,
         CASE WHEN m < 12 THEN 1 WHEN m < 24 THEN 2 WHEN m < 60 THEN 3 ELSE 4 END AS k
  FROM (SELECT date_diff('month', origination_date, DATE '2025-12-31') AS m FROM loan WHERE loan_status='Active')) GROUP BY bucket, k ORDER BY k
