WITH e AS (SELECT loan_id FROM loan_monthly_snapshot GROUP BY 1 HAVING MAX(days_past_due)>=90)
SELECT band, COUNT(*), ROUND(100.0*COUNT(e.loan_id)/COUNT(*),2) FROM (SELECT l.loan_id, CASE WHEN b.bureau_score IS NULL THEN 'no score' WHEN b.bureau_score<600 THEN '<600' WHEN b.bureau_score<700 THEN '600-699' WHEN b.bureau_score<800 THEN '700-799' ELSE '800+' END AS band
 FROM loan l JOIN credit_bureau_report b ON b.application_id=l.application_id AND b.customer_id=l.primary_customer_id) t LEFT JOIN e USING (loan_id) GROUP BY band ORDER BY band
