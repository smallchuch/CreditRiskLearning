SELECT loan_id, lvr_at_origination_pct FROM loan WHERE channel='Mobile Lender' AND loan_status='Active' AND lvr_at_origination_pct > 85 ORDER BY lvr_at_origination_pct DESC, loan_id LIMIT 10
