SELECT l.loan_id, o.price_index, n.price_index, ROUND(100*(n.price_index/o.price_index-1),1)
FROM loan l JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode
JOIN ref_property_price_index o ON o.state=d.state AND o.month_end_date=last_day(l.origination_date)
JOIN ref_property_price_index n ON n.state=d.state AND n.month_end_date=DATE '2025-12-31'
WHERE l.loan_id <= 10 ORDER BY l.loan_id
