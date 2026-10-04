SELECT ROUND(MEDIAN(date_diff('day', default_date, possession_date)/30.44),1), ROUND(MEDIAN(date_diff('day', default_date, sale_date)/30.44),1) FROM loan_loss
