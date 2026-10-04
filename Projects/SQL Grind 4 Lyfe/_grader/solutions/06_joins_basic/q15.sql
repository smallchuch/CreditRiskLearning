SELECT p.product_name, COUNT(*) AS n FROM complaint c JOIN loan l ON l.loan_id=c.loan_id JOIN dim_product p ON p.product_id=l.product_id GROUP BY 1 ORDER BY n DESC, 1
