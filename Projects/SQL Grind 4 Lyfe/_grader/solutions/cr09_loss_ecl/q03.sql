SELECT COUNT(*), ROUND(SUM(ead_at_default),0), ROUND(SUM(net_loss),0), ROUND(AVG(lgd_pct),1) FROM loan_loss
