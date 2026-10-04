CREATE OR REPLACE TABLE scratch.t (id INTEGER, name VARCHAR); INSERT INTO scratch.t VALUES (1,'a'),(2,'b'),(3,'c'); SELECT id, name FROM scratch.t ORDER BY id
