CREATE OR REPLACE TABLE scratch.l AS SELECT loan_id, interest_rate_at_origination_pct AS r FROM loan WHERE loan_id<=5; UPDATE scratch.l SET r = r + 0.50; SELECT loan_id, r FROM scratch.l ORDER BY 1
