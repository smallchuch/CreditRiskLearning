CREATE OR REPLACE TABLE scratch.loans_p2 AS SELECT loan_id, original_amount, origination_date FROM loan WHERE purpose='Refinance'; SELECT COUNT(*), ROUND(SUM(original_amount),0) FROM scratch.loans_p2
