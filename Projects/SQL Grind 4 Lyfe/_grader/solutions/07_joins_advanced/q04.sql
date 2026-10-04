SELECT m.full_name, COUNT(*) AS n FROM dim_staff e JOIN dim_staff m ON m.staff_id=e.manager_staff_id GROUP BY m.staff_id, m.full_name ORDER BY n DESC, 1
