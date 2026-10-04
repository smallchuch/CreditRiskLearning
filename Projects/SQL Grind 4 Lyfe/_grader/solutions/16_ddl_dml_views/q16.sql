CREATE OR REPLACE TABLE scratch.cust_scd (customer_id INTEGER, segment VARCHAR, valid_from DATE, valid_to DATE, is_current BOOLEAN);
INSERT INTO scratch.cust_scd VALUES (1,'Mass',DATE '2020-01-01',NULL,true);
UPDATE scratch.cust_scd SET valid_to=DATE '2023-06-30', is_current=false WHERE customer_id=1 AND is_current;
INSERT INTO scratch.cust_scd VALUES (1,'Premium',DATE '2023-07-01',NULL,true);
SELECT customer_id, segment, valid_from, valid_to, is_current FROM scratch.cust_scd ORDER BY valid_from
