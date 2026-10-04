SELECT COUNT(*) FILTER (WHERE branch_id IS NULL), COUNT(*) FILTER (WHERE broker_id IS NULL) FROM loan WHERE channel='Mobile Lender'
