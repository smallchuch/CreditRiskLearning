SELECT COUNT(*) FILTER (WHERE sale_price<balance_at_sale), ROUND(100.0*COUNT(*) FILTER (WHERE sale_price<balance_at_sale)/COUNT(*),1) FROM loan_loss
