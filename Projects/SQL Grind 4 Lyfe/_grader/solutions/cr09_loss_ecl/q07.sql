SELECT ROUND(SUM(shortfall_before_lmi),0), ROUND(SUM(lmi_recovery),0), ROUND(SUM(net_loss),0), ROUND(100*SUM(lmi_recovery)/SUM(shortfall_before_lmi),1) FROM loan_loss
