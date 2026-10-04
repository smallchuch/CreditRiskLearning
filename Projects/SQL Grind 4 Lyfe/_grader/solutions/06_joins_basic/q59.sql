SELECT l.loan_id, c.segment, p.occupancy FROM loan l JOIN customer c ON c.customer_id=l.primary_customer_id JOIN dim_product p ON p.product_id=l.product_id WHERE l.loan_id<=10 ORDER BY 1
