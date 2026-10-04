SELECT COALESCE(CAST(branch_id AS VARCHAR),'No branch') AS branch_label, COUNT(*) AS loans FROM loan GROUP BY 1 ORDER BY 2 DESC, 1
