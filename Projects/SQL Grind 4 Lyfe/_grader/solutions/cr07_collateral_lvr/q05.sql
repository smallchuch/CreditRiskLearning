SELECT COUNT(DISTINCT property_id) FROM property_valuation WHERE valuation_type='Automated Valuation (AVM)' AND valuation_amount>0 AND valuation_date<=DATE '2025-12-31'
