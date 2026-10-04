SELECT e.staff_id, e.full_name, m.full_name FROM dim_staff e LEFT JOIN dim_staff m ON m.staff_id=e.manager_staff_id WHERE e.staff_id <= 12 ORDER BY 1
