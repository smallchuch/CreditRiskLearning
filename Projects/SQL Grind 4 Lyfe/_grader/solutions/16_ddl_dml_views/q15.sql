CREATE OR REPLACE TABLE scratch.t5 (id INTEGER NOT NULL, amt DOUBLE CHECK (amt >= 0)); INSERT INTO scratch.t5 VALUES (1, 10.5), (2, 0); SELECT id, amt FROM scratch.t5 ORDER BY 1
