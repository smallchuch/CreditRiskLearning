WITH r AS (
  SELECT loan_id, original_amount AS p, term_months AS n, interest_rate_at_origination_pct/1200 AS r0, (interest_rate_at_origination_pct+3)/1200 AS r1
  FROM loan WHERE term_months = 360 AND loan_id <= 40)
SELECT loan_id, ROUND(p*r0/(1-POWER(1+r0,-n)),2) AS base,
       ROUND(p*r1/(1-POWER(1+r1,-n)),2) AS stressed,
       ROUND(100*((p*r1/(1-POWER(1+r1,-n)))/(p*r0/(1-POWER(1+r0,-n)))-1),1) AS pct_increase
FROM r ORDER BY loan_id
