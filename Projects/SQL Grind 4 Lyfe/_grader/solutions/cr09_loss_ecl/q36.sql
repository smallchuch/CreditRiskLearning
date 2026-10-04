SELECT COUNT(*), ROUND(SUM(ead_at_default),0), ROUND(SUM(net_loss),0), ROUND(AVG(lgd_pct),1) FROM loan_loss WHERE default_date >= DATE '2020-01-01' AND default_date < DATE '2021-01-01'
