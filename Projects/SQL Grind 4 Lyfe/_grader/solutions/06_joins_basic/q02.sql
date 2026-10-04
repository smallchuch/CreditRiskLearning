SELECT p.product_name, COUNT(*) AS n FROM loan l JOIN dim_product p USING (product_id) GROUP BY 1 ORDER BY n DESC, 1
