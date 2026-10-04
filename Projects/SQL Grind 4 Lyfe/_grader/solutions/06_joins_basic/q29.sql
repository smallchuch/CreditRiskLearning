SELECT d.state, COUNT(*) FROM loan l JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode WHERE l.channel='Digital' GROUP BY 1 ORDER BY 1
