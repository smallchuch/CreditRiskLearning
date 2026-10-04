SELECT COUNT(*) FROM (SELECT loan_id, ROW_NUMBER() OVER (ORDER BY loan_id) AS rn FROM loan) WHERE rn <> loan_id
