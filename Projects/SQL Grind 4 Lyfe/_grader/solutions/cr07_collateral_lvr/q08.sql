WITH x AS (SELECT s.closing_balance / (l.security_value_at_origination * n.price_index / o.price_index) * 100 AS clvr
 FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode
 JOIN ref_property_price_index o ON o.state=d.state AND o.month_end_date=last_day(l.origination_date) JOIN ref_property_price_index n ON n.state=d.state AND n.month_end_date=DATE '2025-12-31'
 WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed')
SELECT ROUND(100.0*COUNT(*) FILTER (WHERE clvr>80)/COUNT(*),2), ROUND(100.0*COUNT(*) FILTER (WHERE clvr>100)/COUNT(*),2) FROM x
