from . import P

PRIMER = r"""
## Creating things: DDL (structure) and DML (data)

You have a private sandbox schema called **`scratch`** (an in-memory database, wiped every run) so you can never damage the bank database.
Always write `scratch.table_name`.

```
 CREATE TABLE scratch.t AS SELECT ...                     -- build a table from a query (CTAS)
 CREATE OR REPLACE TABLE scratch.t AS SELECT ...          -- same, re-runnable
 CREATE VIEW scratch.v AS SELECT ...                      -- saved query, no data stored
 CREATE TABLE scratch.t (id INTEGER, name VARCHAR);       -- empty table with a schema
 INSERT INTO scratch.t VALUES (1,'a'), (2,'b');
 UPDATE scratch.t SET name = 'z' WHERE id = 1;
 DELETE FROM scratch.t WHERE id = 2;
 ALTER TABLE scratch.t ADD COLUMN flag BOOLEAN;
```
**Your answer must END with a SELECT** that shows the final state - that is what gets checked. Run several statements in one `.sql` file separated by semicolons.

Concepts: **table vs view** (stored data vs stored query) | **temp tables** for step-by-step work | **upsert** (`INSERT ... ON CONFLICT`) | **constraints** (primary key, NOT NULL, CHECK) | **transactions** (`BEGIN; ...; COMMIT;`) | **idempotent scripts** (`CREATE OR REPLACE`, `DROP IF EXISTS`) so they can be re-run safely.
"""

CONCEPT = dict(id="16_ddl_dml_views", title="16 - CREATE, INSERT, UPDATE, DELETE, VIEWs (in the scratch sandbox)", primer=PRIMER, problems=[
    P(1, "Create `scratch.big_loans` as a table of loans over $2,000,000 (`loan_id`, `original_amount`), then SELECT the row count. One number.",
      "CREATE OR REPLACE TABLE scratch.big_loans AS SELECT loan_id, original_amount FROM loan WHERE original_amount > 2000000; SELECT COUNT(*) FROM scratch.big_loans"),
    P(1, "Create `scratch.t` with columns `id INTEGER`, `name VARCHAR`, insert (1,'a'), (2,'b'), (3,'c'), then SELECT `id`, `name` sorted by id.",
      "CREATE OR REPLACE TABLE scratch.t (id INTEGER, name VARCHAR); INSERT INTO scratch.t VALUES (1,'a'),(2,'b'),(3,'c'); SELECT id, name FROM scratch.t ORDER BY id"),
    P(1, "Create a VIEW `scratch.v_active` over `loan` for Active loans (`loan_id`, `product_id`, `original_amount`), then count its rows. One number.",
      "CREATE OR REPLACE VIEW scratch.v_active AS SELECT loan_id, product_id, original_amount FROM loan WHERE loan_status='Active'; SELECT COUNT(*) FROM scratch.v_active"),
    P(2, "Create `scratch.prod_summary` (`product_id`, `loans`, `total_amount` rounded to 0dp) from `loan`, then SELECT it for product ids 1-5 sorted by `product_id`.",
      "CREATE OR REPLACE TABLE scratch.prod_summary AS SELECT product_id, COUNT(*) AS loans, ROUND(SUM(original_amount),0) AS total_amount FROM loan GROUP BY 1; SELECT * FROM scratch.prod_summary WHERE product_id <= 5 ORDER BY 1"),
    P(2, "UPDATE practice: copy loans 1-5 to `scratch.l` (`loan_id`, `interest_rate_at_origination_pct`), then add 0.50 to every rate with an UPDATE, then SELECT `loan_id`, rate sorted by `loan_id`.",
      "CREATE OR REPLACE TABLE scratch.l AS SELECT loan_id, interest_rate_at_origination_pct AS r FROM loan WHERE loan_id<=5; UPDATE scratch.l SET r = r + 0.50; SELECT loan_id, r FROM scratch.l ORDER BY 1"),
    P(2, "DELETE practice: copy loans 1-20 to `scratch.l2` (`loan_id`, `original_amount`), DELETE those with amount below 400,000, then SELECT the remaining row count. One number.",
      "CREATE OR REPLACE TABLE scratch.l2 AS SELECT loan_id, original_amount FROM loan WHERE loan_id<=20; DELETE FROM scratch.l2 WHERE original_amount < 400000; SELECT COUNT(*) FROM scratch.l2"),
    P(2, "ALTER + UPDATE: create `scratch.l3` from loans 1-6 (`loan_id`, `original_amount`), ADD COLUMN `size_band` VARCHAR, set it with an UPDATE to `'Large'` where amount >= 600000 else `'Standard'`, then SELECT `loan_id`, `size_band` sorted by `loan_id`.",
      "CREATE OR REPLACE TABLE scratch.l3 AS SELECT loan_id, original_amount FROM loan WHERE loan_id<=6; ALTER TABLE scratch.l3 ADD COLUMN size_band VARCHAR; UPDATE scratch.l3 SET size_band = CASE WHEN original_amount >= 600000 THEN 'Large' ELSE 'Standard' END; SELECT loan_id, size_band FROM scratch.l3 ORDER BY 1"),
    P(2, "A view with logic: `scratch.v_loan_lvr_band` giving `loan_id` and a CASE band `'<=80'`, `'80-90'`, `'>90'`. Then SELECT band counts: `band`, `loans`; sorted by band.",
      "CREATE OR REPLACE VIEW scratch.v_loan_lvr_band AS SELECT loan_id, CASE WHEN lvr_at_origination_pct<=80 THEN '<=80' WHEN lvr_at_origination_pct<=90 THEN '80-90' ELSE '>90' END AS band FROM loan; SELECT band, COUNT(*) FROM scratch.v_loan_lvr_band GROUP BY 1 ORDER BY 1"),
    P(2, "INSERT ... SELECT: create an empty `scratch.hist` (`loan_id INTEGER`, `bal DOUBLE`), insert the 2025-12-31 closing balances for loans 1-50 that are non-closed, then SELECT `COUNT(*)` and `ROUND(SUM(bal),0)`.",
      "CREATE OR REPLACE TABLE scratch.hist (loan_id INTEGER, bal DOUBLE); INSERT INTO scratch.hist SELECT loan_id, closing_balance FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed' AND loan_id<=50; SELECT COUNT(*), ROUND(SUM(bal),0) FROM scratch.hist"),
    P(2, "Clean copy of customers: create `scratch.cust_clean` with `customer_id`, `state_clean` (upper-cased, no dots/spaces, mapped full names to codes as in earlier problems - use the mapping for 'SOUTHAUSTRALIA'->'SA', 'VICTORIA'->'VIC', 'NEWSOUTHWALES'->'NSW' only), `email_clean` (lowercase). Then SELECT `state_clean`, count for the states 'SA' and 'VIC' and 'NSW' sorted by state.",
      """CREATE OR REPLACE TABLE scratch.cust_clean AS SELECT customer_id, CASE s WHEN 'SOUTHAUSTRALIA' THEN 'SA' WHEN 'VICTORIA' THEN 'VIC' WHEN 'NEWSOUTHWALES' THEN 'NSW' ELSE s END AS state_clean, LOWER(email) AS email_clean FROM (SELECT customer_id, UPPER(REPLACE(REPLACE(state,'.',''),' ','')) AS s, email FROM customer);
SELECT state_clean, COUNT(*) FROM scratch.cust_clean WHERE state_clean IN ('SA','VIC','NSW') GROUP BY 1 ORDER BY 1"""),
    P(3, "Upsert: create `scratch.limits (staff_id INTEGER PRIMARY KEY, lim INTEGER)` filled from `dim_staff` for staff 1-5 (`lending_authority_limit`). Then `INSERT ... ON CONFLICT (staff_id) DO UPDATE SET lim = excluded.lim` for rows (3, 999999), (6, 123456). SELECT `staff_id`, `lim` sorted by `staff_id` for ids 1-6.",
      """CREATE OR REPLACE TABLE scratch.limits (staff_id INTEGER PRIMARY KEY, lim INTEGER);
INSERT INTO scratch.limits SELECT staff_id, lending_authority_limit FROM dim_staff WHERE staff_id<=5;
INSERT INTO scratch.limits VALUES (3, 999999), (6, 123456) ON CONFLICT (staff_id) DO UPDATE SET lim = excluded.lim;
SELECT staff_id, lim FROM scratch.limits ORDER BY 1"""),
    P(3, "Staging pattern: build `scratch.stg_latest_snapshot` (`loan_id`, `closing_balance`, `days_past_due`) for non-closed loans at 2025-12-31, then `scratch.arrears_summary` from it with `bucket` ('Current','1-29','30-89','90+') and `loans`, `balance` (0dp). SELECT from the summary sorted by loans descending... then bucket.",
      """CREATE OR REPLACE TABLE scratch.stg_latest_snapshot AS SELECT loan_id, closing_balance, days_past_due FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed';
CREATE OR REPLACE TABLE scratch.arrears_summary AS SELECT CASE WHEN days_past_due=0 THEN 'Current' WHEN days_past_due<30 THEN '1-29' WHEN days_past_due<90 THEN '30-89' ELSE '90+' END AS bucket, COUNT(*) AS loans, ROUND(SUM(closing_balance),0) AS balance FROM scratch.stg_latest_snapshot GROUP BY 1;
SELECT bucket, loans, balance FROM scratch.arrears_summary ORDER BY loans DESC, bucket"""),
    P(3, "Views over views: `scratch.v1` = loans with `original_amount > 1000000`; `scratch.v2` = v1 joined to `dim_product` giving `product_name` and `loan_id`. SELECT `product_name`, `loans` from v2 sorted by loans descending, then product_name, top 5 rows.",
      "CREATE OR REPLACE VIEW scratch.v1 AS SELECT loan_id, product_id FROM loan WHERE original_amount > 1000000; CREATE OR REPLACE VIEW scratch.v2 AS SELECT v.loan_id, p.product_name FROM scratch.v1 v JOIN dim_product p USING (product_id); SELECT product_name, COUNT(*) AS loans FROM scratch.v2 GROUP BY 1 ORDER BY loans DESC, 1 LIMIT 5"),
    P(3, "A reusable calendar: create `scratch.cal` with one row per month-end 2025 (`month_end DATE`) using generate_series, and `scratch.monthly_loans` joining origination counts. SELECT `month_end`, `loans` sorted by month_end.",
      """CREATE OR REPLACE TABLE scratch.cal AS SELECT CAST(last_day(unnest(generate_series(DATE '2025-01-01', DATE '2025-12-01', INTERVAL 1 MONTH))) AS DATE) AS month_end;
CREATE OR REPLACE TABLE scratch.monthly_loans AS SELECT c.month_end, COUNT(l.loan_id) AS loans FROM scratch.cal c LEFT JOIN loan l ON last_day(l.origination_date)=c.month_end GROUP BY 1;
SELECT month_end, loans FROM scratch.monthly_loans ORDER BY 1"""),
    P(3, "Constraint check: create `scratch.t5 (id INTEGER NOT NULL, amt DOUBLE CHECK (amt >= 0))`, insert (1, 10.5), (2, 0), then SELECT `id`, `amt` sorted by id. (Think: what would happen if you inserted a negative amount?)",
      "CREATE OR REPLACE TABLE scratch.t5 (id INTEGER NOT NULL, amt DOUBLE CHECK (amt >= 0)); INSERT INTO scratch.t5 VALUES (1, 10.5), (2, 0); SELECT id, amt FROM scratch.t5 ORDER BY 1"),
    P(3, "Slowly changing dimension (type 2) by hand: create `scratch.cust_scd (customer_id, segment, valid_from DATE, valid_to DATE, is_current BOOLEAN)` with (1,'Mass','2020-01-01',NULL,true). Then close that row (`valid_to='2023-06-30'`, `is_current=false`) and insert (1,'Premium','2023-07-01',NULL,true). SELECT all rows sorted by `valid_from`.",
      """CREATE OR REPLACE TABLE scratch.cust_scd (customer_id INTEGER, segment VARCHAR, valid_from DATE, valid_to DATE, is_current BOOLEAN);
INSERT INTO scratch.cust_scd VALUES (1,'Mass',DATE '2020-01-01',NULL,true);
UPDATE scratch.cust_scd SET valid_to=DATE '2023-06-30', is_current=false WHERE customer_id=1 AND is_current;
INSERT INTO scratch.cust_scd VALUES (1,'Premium',DATE '2023-07-01',NULL,true);
SELECT customer_id, segment, valid_from, valid_to, is_current FROM scratch.cust_scd ORDER BY valid_from"""),
])
