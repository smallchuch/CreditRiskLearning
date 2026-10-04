SELECT l.loan_id, b.branch_name FROM loan l LEFT JOIN dim_branch b ON b.branch_id=l.branch_id WHERE l.loan_id <= 10 ORDER BY l.loan_id
