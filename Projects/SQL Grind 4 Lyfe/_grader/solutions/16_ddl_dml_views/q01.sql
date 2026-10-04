CREATE OR REPLACE TABLE scratch.big_loans AS SELECT loan_id, original_amount FROM loan WHERE original_amount > 2000000; SELECT COUNT(*) FROM scratch.big_loans
