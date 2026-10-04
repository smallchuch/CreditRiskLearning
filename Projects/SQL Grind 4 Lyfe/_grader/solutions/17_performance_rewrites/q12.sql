SELECT ROUND(SUM(closing_balance),0) FROM (SELECT closing_balance FROM loan_monthly_snapshot WHERE loan_id<=100 QUALIFY ROW_NUMBER() OVER (PARTITION BY loan_id ORDER BY snapshot_date DESC)=1)
