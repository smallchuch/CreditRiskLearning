SELECT l.loan_id, p.product_name FROM loan l JOIN dim_product p ON p.product_id=l.product_id WHERE l.loan_id <= 10 ORDER BY l.loan_id
