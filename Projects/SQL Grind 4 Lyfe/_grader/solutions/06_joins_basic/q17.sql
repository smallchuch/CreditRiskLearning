SELECT l.loan_id, l.security_value_at_origination, v.valuation_amount FROM loan l
JOIN property_valuation v ON v.property_id=l.property_id
WHERE l.loan_id <= 10 AND v.valuation_amount > 0
  AND v.valuation_date = (SELECT MAX(v2.valuation_date) FROM property_valuation v2 WHERE v2.property_id=l.property_id AND v2.valuation_amount>0 AND v2.valuation_date <= DATE '2025-12-31')
ORDER BY l.loan_id
