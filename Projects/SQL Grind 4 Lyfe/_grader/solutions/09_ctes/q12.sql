WITH RECURSIVE c AS (
  SELECT loan_id AS root, loan_id, 1 AS len FROM loan WHERE parent_loan_id IS NULL AND EXISTS (SELECT 1 FROM loan k WHERE k.parent_loan_id=loan.loan_id)
  UNION ALL SELECT c.root, l.loan_id, c.len+1 FROM loan l JOIN c ON l.parent_loan_id=c.loan_id)
SELECT mx, COUNT(*) FROM (SELECT root, MAX(len) AS mx FROM c GROUP BY 1) GROUP BY 1 ORDER BY 1
