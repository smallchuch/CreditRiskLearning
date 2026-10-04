SELECT e.staff_id, e.full_name, m.full_name, m.team FROM dim_staff e JOIN dim_staff m ON m.staff_id=e.manager_staff_id WHERE e.team='Broker Credit' ORDER BY e.staff_id LIMIT 10
