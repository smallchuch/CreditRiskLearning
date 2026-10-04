SELECT product_id, CASE WHEN rate_type='Fixed' THEN 'Fixed ' || fixed_term_months || 'm' ELSE 'Variable' END FROM dim_product ORDER BY product_id
