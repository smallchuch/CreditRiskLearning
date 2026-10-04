SELECT staff_id, full_name, team, termination_date FROM dim_staff WHERE termination_date >= DATE '2024-01-01' AND termination_date < DATE '2025-01-01' ORDER BY termination_date, staff_id
