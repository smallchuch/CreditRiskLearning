SELECT hardship_type, ROUND(AVG(planned_length_months),1) FROM hardship_arrangement WHERE hardship_type<>'COVID-19 repayment deferral' GROUP BY 1 ORDER BY 1
