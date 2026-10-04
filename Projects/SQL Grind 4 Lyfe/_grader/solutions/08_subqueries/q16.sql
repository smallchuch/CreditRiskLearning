SELECT branch_id, n FROM (SELECT branch_id, COUNT(*) AS n FROM loan WHERE loan_status='Active' AND branch_id IS NOT NULL GROUP BY 1)
WHERE n > (SELECT MEDIAN(n) FROM (SELECT COUNT(*) AS n FROM loan WHERE loan_status='Active' AND branch_id IS NOT NULL GROUP BY branch_id)) ORDER BY n DESC, 1
