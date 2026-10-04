SELECT loan_id, origination_date FROM loan WHERE dayofweek(origination_date) IN (0,6) ORDER BY loan_id
