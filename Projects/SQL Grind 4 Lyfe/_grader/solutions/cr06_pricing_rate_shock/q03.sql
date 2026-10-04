SELECT year(event_date), COUNT(*) FROM loan_event WHERE event_type='Fixed rate expired - reverted to variable' GROUP BY 1 ORDER BY 1
