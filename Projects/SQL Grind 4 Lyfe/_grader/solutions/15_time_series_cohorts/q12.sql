WITH k AS (SELECT unnest([6,12,18,24]) AS mob)
SELECT k.mob, COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE e.mx>=30)/COUNT(*),2) FROM k JOIN (
  SELECT l.loan_id, s.months_on_book AS mob, MAX(s2.days_past_due) AS mx FROM loan l
  JOIN loan_monthly_snapshot s ON s.loan_id=l.loan_id JOIN loan_monthly_snapshot s2 ON s2.loan_id=l.loan_id AND s2.months_on_book<=s.months_on_book
  WHERE year(l.origination_date)=2022 AND s.months_on_book IN (6,12,18,24) GROUP BY 1,2) e ON e.mob=k.mob GROUP BY k.mob ORDER BY k.mob
