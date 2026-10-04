SELECT channel, loans FROM (SELECT channel, COUNT(*) AS loans FROM loan GROUP BY 1 UNION ALL SELECT 'ALL', COUNT(*) FROM loan) ORDER BY channel='ALL', channel
