SELECT COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=30)/COUNT(*),1) FROM hardship_arrangement h JOIN loan_monthly_snapshot s ON s.loan_id=h.loan_id AND s.snapshot_date=last_day(h.end_date + INTERVAL 6 MONTH)
WHERE h.hardship_type<>'COVID-19 repayment deferral' AND h.end_date<=DATE '2025-06-30' AND s.loan_status<>'Closed'
