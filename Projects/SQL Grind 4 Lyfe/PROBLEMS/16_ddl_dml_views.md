# 16 - CREATE, INSERT, UPDATE, DELETE, VIEWs (in the scratch sandbox)

`answers/16_ddl_dml_views/qNN.sql` &nbsp;|&nbsp; check with: `grade 16` or `grade 16 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

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

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Create `scratch.big_loans` as a table of loans over $2,000,000 (`loan_id`, `original_amount`), then SELECT the row count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Create `scratch.t` with columns `id INTEGER`, `name VARCHAR`, insert (1,'a'), (2,'b'), (3,'c'), then SELECT `id`, `name` sorted by id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Create a VIEW `scratch.v_active` over `loan` for Active loans (`loan_id`, `product_id`, `original_amount`), then count its rows. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q04 &nbsp; ★★ &nbsp; (core)

Create `scratch.prod_summary` (`product_id`, `loans`, `total_amount` rounded to 0dp) from `loan`, then SELECT it for product ids 1-5 sorted by `product_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

UPDATE practice: copy loans 1-5 to `scratch.l` (`loan_id`, `interest_rate_at_origination_pct`), then add 0.50 to every rate with an UPDATE, then SELECT `loan_id`, rate sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

DELETE practice: copy loans 1-20 to `scratch.l2` (`loan_id`, `original_amount`), DELETE those with amount below 400,000, then SELECT the remaining row count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q07 &nbsp; ★★ &nbsp; (core)

ALTER + UPDATE: create `scratch.l3` from loans 1-6 (`loan_id`, `original_amount`), ADD COLUMN `size_band` VARCHAR, set it with an UPDATE to `'Large'` where amount >= 600000 else `'Standard'`, then SELECT `loan_id`, `size_band` sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

A view with logic: `scratch.v_loan_lvr_band` giving `loan_id` and a CASE band `'<=80'`, `'80-90'`, `'>90'`. Then SELECT band counts: `band`, `loans`; sorted by band.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

INSERT ... SELECT: create an empty `scratch.hist` (`loan_id INTEGER`, `bal DOUBLE`), insert the 2025-12-31 closing balances for loans 1-50 that are non-closed, then SELECT `COUNT(*)` and `ROUND(SUM(bal),0)`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q10 &nbsp; ★★ &nbsp; (core)

Clean copy of customers: create `scratch.cust_clean` with `customer_id`, `state_clean` (upper-cased, no dots/spaces, mapped full names to codes as in earlier problems - use the mapping for 'SOUTHAUSTRALIA'->'SA', 'VICTORIA'->'VIC', 'NEWSOUTHWALES'->'NSW' only), `email_clean` (lowercase). Then SELECT `state_clean`, count for the states 'SA' and 'VIC' and 'NSW' sorted by state.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Upsert: create `scratch.limits (staff_id INTEGER PRIMARY KEY, lim INTEGER)` filled from `dim_staff` for staff 1-5 (`lending_authority_limit`). Then `INSERT ... ON CONFLICT (staff_id) DO UPDATE SET lim = excluded.lim` for rows (3, 999999), (6, 123456). SELECT `staff_id`, `lim` sorted by `staff_id` for ids 1-6.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Staging pattern: build `scratch.stg_latest_snapshot` (`loan_id`, `closing_balance`, `days_past_due`) for non-closed loans at 2025-12-31, then `scratch.arrears_summary` from it with `bucket` ('Current','1-29','30-89','90+') and `loans`, `balance` (0dp). SELECT from the summary sorted by loans descending... then bucket.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

Views over views: `scratch.v1` = loans with `original_amount > 1000000`; `scratch.v2` = v1 joined to `dim_product` giving `product_name` and `loan_id`. SELECT `product_name`, `loans` from v2 sorted by loans descending, then product_name, top 5 rows.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

A reusable calendar: create `scratch.cal` with one row per month-end 2025 (`month_end DATE`) using generate_series, and `scratch.monthly_loans` joining origination counts. SELECT `month_end`, `loans` sorted by month_end.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★★ &nbsp; (challenge)

Constraint check: create `scratch.t5 (id INTEGER NOT NULL, amt DOUBLE CHECK (amt >= 0))`, insert (1, 10.5), (2, 0), then SELECT `id`, `amt` sorted by id. (Think: what would happen if you inserted a negative amount?)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★★ &nbsp; (challenge)

Slowly changing dimension (type 2) by hand: create `scratch.cust_scd (customer_id, segment, valid_from DATE, valid_to DATE, is_current BOOLEAN)` with (1,'Mass','2020-01-01',NULL,true). Then close that row (`valid_to='2023-06-30'`, `is_current=false`) and insert (1,'Premium','2023-07-01',NULL,true). SELECT all rows sorted by `valid_from`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q17 &nbsp; ★ &nbsp; (warm-up)

Create `scratch.loans_p0` as a copy of loans with purpose `'Purchase - Owner Occupied'` (`loan_id`, `original_amount`, `origination_date`), then SELECT its row count and total amount (0 dp). `loans`, `total`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★ &nbsp; (warm-up)

Create `scratch.loans_p1` as a copy of loans with purpose `'Purchase - Investment'` (`loan_id`, `original_amount`, `origination_date`), then SELECT its row count and total amount (0 dp). `loans`, `total`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★ &nbsp; (warm-up)

Create `scratch.loans_p2` as a copy of loans with purpose `'Refinance'` (`loan_id`, `original_amount`, `origination_date`), then SELECT its row count and total amount (0 dp). `loans`, `total`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★ &nbsp; (warm-up)

Create `scratch.loans_p3` as a copy of loans with purpose `'Equity Release / Top-up'` (`loan_id`, `original_amount`, `origination_date`), then SELECT its row count and total amount (0 dp). `loans`, `total`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★ &nbsp; (warm-up)

Create `scratch.loans_p4` as a copy of loans with purpose `'Construction'` (`loan_id`, `original_amount`, `origination_date`), then SELECT its row count and total amount (0 dp). `loans`, `total`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★ &nbsp; (core)

Create a VIEW `scratch.v_ch0` of loans via `'Broker'` showing `loan_id`, `product_id`, `original_amount`; then SELECT from it the number of loans per product for products 1-5. `product_id`, `loans`; sorted by product_id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q23 &nbsp; ★★ &nbsp; (core)

Create a VIEW `scratch.v_ch1` of loans via `'Branch'` showing `loan_id`, `product_id`, `original_amount`; then SELECT from it the number of loans per product for products 1-5. `product_id`, `loans`; sorted by product_id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q24 &nbsp; ★★ &nbsp; (core)

Create a VIEW `scratch.v_ch2` of loans via `'Digital'` showing `loan_id`, `product_id`, `original_amount`; then SELECT from it the number of loans per product for products 1-5. `product_id`, `loans`; sorted by product_id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q25 &nbsp; ★★ &nbsp; (core)

Create a VIEW `scratch.v_ch3` of loans via `'Mobile Lender'` showing `loan_id`, `product_id`, `original_amount`; then SELECT from it the number of loans per product for products 1-5. `product_id`, `loans`; sorted by product_id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q26 &nbsp; ★★ &nbsp; (core)

UPDATE with CASE: copy loans 1-20 to `scratch.u0` (`loan_id`, `original_amount`), UPDATE a new `flag` column to `'big'` where amount >= 100000 else `'small'`, then SELECT `flag`, `n` counts; sorted by flag.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q27 &nbsp; ★★ &nbsp; (core)

UPDATE with CASE: copy loans 1-20 to `scratch.u1` (`loan_id`, `original_amount`), UPDATE a new `flag` column to `'big'` where amount >= 250000 else `'small'`, then SELECT `flag`, `n` counts; sorted by flag.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q28 &nbsp; ★★ &nbsp; (core)

UPDATE with CASE: copy loans 1-20 to `scratch.u2` (`loan_id`, `original_amount`), UPDATE a new `flag` column to `'big'` where amount >= 500000 else `'small'`, then SELECT `flag`, `n` counts; sorted by flag.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q29 &nbsp; ★★ &nbsp; (core)

UPDATE with CASE: copy loans 1-20 to `scratch.u3` (`loan_id`, `original_amount`), UPDATE a new `flag` column to `'big'` where amount >= 1000000 else `'small'`, then SELECT `flag`, `n` counts; sorted by flag.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q30 &nbsp; ★★ &nbsp; (core)

DELETE then count: copy loans originated in 2021 to `scratch.d0`, delete those over $900,000, then SELECT the remaining count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q31 &nbsp; ★★ &nbsp; (core)

DELETE then count: copy loans originated in 2023 to `scratch.d1`, delete those over $900,000, then SELECT the remaining count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q32 &nbsp; ★★ &nbsp; (core)

DELETE then count: copy loans originated in 2025 to `scratch.d2`, delete those over $900,000, then SELECT the remaining count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q33 &nbsp; ★★★ &nbsp; (challenge)

Summary table: create `scratch.s0` with the number of live loans and total balance (0 dp) at 2025-12-31 by `purpose` for property state `'NSW'`, then SELECT it sorted by purpose. `purpose`, `loans`, `balance`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★★★ &nbsp; (challenge)

Summary table: create `scratch.s1` with the number of live loans and total balance (0 dp) at 2025-12-31 by `purpose` for property state `'VIC'`, then SELECT it sorted by purpose. `purpose`, `loans`, `balance`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★★★ &nbsp; (challenge)

Summary table: create `scratch.s2` with the number of live loans and total balance (0 dp) at 2025-12-31 by `purpose` for property state `'QLD'`, then SELECT it sorted by purpose. `purpose`, `loans`, `balance`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q36 &nbsp; ★★★ &nbsp; (challenge)

Summary table: create `scratch.s3` with the number of live loans and total balance (0 dp) at 2025-12-31 by `purpose` for property state `'SA'`, then SELECT it sorted by purpose. `purpose`, `loans`, `balance`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.
