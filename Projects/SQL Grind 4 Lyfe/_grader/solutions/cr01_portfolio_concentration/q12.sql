SELECT state, product_name, ROUND(b,0) FROM (SELECT d.state, p.product_name, SUM(s.closing_balance) AS b, ROW_NUMBER() OVER (PARTITION BY d.state ORDER BY SUM(s.closing_balance) DESC, p.product_name) AS rn
FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property pr ON pr.property_id=l.property_id JOIN dim_postcode d ON d.postcode=pr.postcode JOIN dim_product p ON p.product_id=l.product_id
WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1,2) WHERE rn=1 ORDER BY 1
