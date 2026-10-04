SELECT loan_id, purpose FROM loan WHERE purpose NOT IN ('Purchase - Owner Occupied','Refinance') AND origination_date >= DATE '2025-12-01' AND origination_date <= DATE '2025-12-31' ORDER BY loan_id
