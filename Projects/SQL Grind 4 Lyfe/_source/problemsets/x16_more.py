from ._gen import *
MORE_FOR = '16_ddl_dml_views'
PROBLEMS = []
for i,p in enumerate(EXT_PURPOSES):
    PROBLEMS.append(P(1, f"Create `scratch.loans_p{i}` as a copy of loans with purpose `'{p}'` (`loan_id`, `original_amount`, `origination_date`), then SELECT its row count and total amount (0 dp). `loans`, `total`.",
      f"CREATE OR REPLACE TABLE scratch.loans_p{i} AS SELECT loan_id, original_amount, origination_date FROM loan WHERE purpose='{p}'; SELECT COUNT(*), ROUND(SUM(original_amount),0) FROM scratch.loans_p{i}"))
for i,c in enumerate(CHANNELS):
    PROBLEMS.append(P(2, f"Create a VIEW `scratch.v_ch{i}` of loans via `'{c}'` showing `loan_id`, `product_id`, `original_amount`; then SELECT from it the number of loans per product for products 1-5. `product_id`, `loans`; sorted by product_id.",
      f"CREATE OR REPLACE VIEW scratch.v_ch{i} AS SELECT loan_id, product_id, original_amount FROM loan WHERE channel='{c}'; SELECT product_id, COUNT(*) FROM scratch.v_ch{i} WHERE product_id<=5 GROUP BY 1 ORDER BY 1"))
for i,amt in enumerate((100,250,500,1000)):
    PROBLEMS.append(P(2, f"UPDATE with CASE: copy loans 1-20 to `scratch.u{i}` (`loan_id`, `original_amount`), UPDATE a new `flag` column to `'big'` where amount >= {amt}000 else `'small'`, then SELECT `flag`, `n` counts; sorted by flag.",
      f"CREATE OR REPLACE TABLE scratch.u{i} AS SELECT loan_id, original_amount, CAST(NULL AS VARCHAR) AS flag FROM loan WHERE loan_id<=20; UPDATE scratch.u{i} SET flag = CASE WHEN original_amount >= {amt}000 THEN 'big' ELSE 'small' END; SELECT flag, COUNT(*) FROM scratch.u{i} GROUP BY 1 ORDER BY 1"))
for i,y in enumerate((2021,2023,2025)):
    PROBLEMS.append(P(2, f"DELETE then count: copy loans originated in {y} to `scratch.d{i}`, delete those over $900,000, then SELECT the remaining count. One number.",
      f"CREATE OR REPLACE TABLE scratch.d{i} AS SELECT loan_id, original_amount FROM loan WHERE {yr('origination_date',y)}; DELETE FROM scratch.d{i} WHERE original_amount>900000; SELECT COUNT(*) FROM scratch.d{i}"))
for i,s in enumerate(('NSW','VIC','QLD','SA')):
    PROBLEMS.append(P(3, f"Summary table: create `scratch.s{i}` with the number of live loans and total balance (0 dp) at 2025-12-31 by `purpose` for property state `'{s}'`, then SELECT it sorted by purpose. `purpose`, `loans`, `balance`.",
      f"CREATE OR REPLACE TABLE scratch.s{i} AS SELECT l.purpose, COUNT(*) AS loans, ROUND(SUM(m.closing_balance),0) AS balance FROM loan_monthly_snapshot m JOIN loan l USING (loan_id) JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode WHERE m.snapshot_date=DATE '2025-12-31' AND m.loan_status<>'Closed' AND d.state='{s}' GROUP BY 1; SELECT purpose, loans, balance FROM scratch.s{i} ORDER BY 1"))
