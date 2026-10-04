SELECT d.state, s.loan_id, s.closing_balance FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode
WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed'
QUALIFY ROW_NUMBER() OVER (PARTITION BY d.state ORDER BY s.closing_balance DESC, s.loan_id)=1 ORDER BY 1
