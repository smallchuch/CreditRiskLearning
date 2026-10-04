CREATE OR REPLACE TABLE scratch.l2 AS SELECT loan_id, original_amount FROM loan WHERE loan_id<=20; DELETE FROM scratch.l2 WHERE original_amount < 400000; SELECT COUNT(*) FROM scratch.l2
