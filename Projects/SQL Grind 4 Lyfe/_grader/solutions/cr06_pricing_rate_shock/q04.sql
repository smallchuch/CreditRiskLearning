SELECT bank_effective_date - decision_date, COUNT(*) FROM ref_rba_cash_rate GROUP BY 1 ORDER BY 1
