SELECT state, ROUND(100.0*n30/n,2) FROM (
 SELECT d.state, COUNT(*) AS n, COUNT(*) FILTER (WHERE s.days_past_due>=30) AS n30
 FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode
 WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1) ORDER BY 1
