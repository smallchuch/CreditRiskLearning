SELECT pr.product_name, COUNT(*) AS n FROM loan l JOIN dim_product pr USING (product_id) WHERE l.purpose='Construction' GROUP BY 1 ORDER BY n DESC, 1 LIMIT 3
