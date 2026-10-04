SELECT * FROM (SELECT loan_id, original_amount, ROW_NUMBER() OVER (ORDER BY original_amount DESC, loan_id) AS rn FROM loan) WHERE rn <= 10 ORDER BY rn
