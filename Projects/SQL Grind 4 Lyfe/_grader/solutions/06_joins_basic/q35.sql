SELECT b.branch_name, COUNT(*) AS n FROM loan l JOIN dim_branch b USING (branch_id) WHERE b.state='WA' GROUP BY b.branch_id, b.branch_name ORDER BY n DESC, 1 LIMIT 5
