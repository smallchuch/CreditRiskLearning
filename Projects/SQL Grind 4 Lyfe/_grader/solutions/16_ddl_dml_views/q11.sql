CREATE OR REPLACE TABLE scratch.limits (staff_id INTEGER PRIMARY KEY, lim INTEGER);
INSERT INTO scratch.limits SELECT staff_id, lending_authority_limit FROM dim_staff WHERE staff_id<=5;
INSERT INTO scratch.limits VALUES (3, 999999), (6, 123456) ON CONFLICT (staff_id) DO UPDATE SET lim = excluded.lim;
SELECT staff_id, lim FROM scratch.limits ORDER BY 1
