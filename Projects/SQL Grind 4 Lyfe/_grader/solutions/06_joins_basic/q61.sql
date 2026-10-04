SELECT b.region, COUNT(*) AS n FROM complaint c JOIN loan l USING (loan_id) JOIN dim_branch b ON b.branch_id=l.branch_id GROUP BY 1 ORDER BY n DESC, 1
