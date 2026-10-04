SELECT event_type, COUNT(*) AS n FROM loan_event WHERE event_date >= DATE '2025-01-01' AND event_date < DATE '2026-01-01' GROUP BY 1 ORDER BY n DESC, 1
