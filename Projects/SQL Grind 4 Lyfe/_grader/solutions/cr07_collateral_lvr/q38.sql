SELECT COUNT(*), ROUND(AVG(valuation_amount),0), COUNT(*) FILTER (WHERE valuation_amount=0) FROM property_valuation WHERE valuation_type='Origination - Desktop'
