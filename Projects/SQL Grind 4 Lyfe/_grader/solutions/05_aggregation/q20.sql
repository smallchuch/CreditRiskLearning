SELECT p.state, ROUND(100.0*SUM(s.closing_balance)/SUM(SUM(s.closing_balance)) OVER (),1) AS sh
FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property pr ON pr.property_id=l.property_id JOIN dim_postcode p ON p.postcode=pr.postcode
WHERE s.snapshot_date = DATE '2025-12-31' AND s.loan_status='Active' GROUP BY 1 ORDER BY sh DESC, 1
