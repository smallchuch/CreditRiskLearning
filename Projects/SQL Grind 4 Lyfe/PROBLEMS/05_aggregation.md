# 05 - Aggregation: GROUP BY, HAVING, conditional aggregates

`answers/05_aggregation/qNN.sql` &nbsp;|&nbsp; check with: `grade 05` or `grade 05 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## GROUP BY = fold many rows into one row per group

```
 loan rows                          GROUP BY purpose                result
 purpose     amount                 +-----------------------+
 Refinance   500k   --+            | Refinance  : 500,700   |      purpose     n   total
 Refinance   700k   --+--> bucket  +-----------------------+      Refinance   2   1.2m
 Construct.  300k   ----> bucket   | Construct. : 300       |      Construct.  1   0.3m
```

| Function | Meaning | NULLs |
|---|---|---|
| `COUNT(*)` | rows | counts all |
| `COUNT(x)` | non-NULL x | skips |
| `COUNT(DISTINCT x)` | unique x | skips |
| `SUM/AVG/MIN/MAX` | as named | skip |
| `COUNT(*) FILTER (WHERE cond)` | conditional count | - |
| `MEDIAN(x)`, `QUANTILE_CONT(x, 0.9)` | statistics | skip |

**WHERE vs HAVING**: `WHERE` filters rows *before* grouping; `HAVING` filters groups *after*.

```
 FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
```

**Rule:** every column in `SELECT` must be either in `GROUP BY` or inside an aggregate.
`GROUP BY ALL` (DuckDB) groups by all non-aggregated select columns - great for quick work.

**Weighted average** (credit risk staple): `SUM(x*w)/SUM(w)`, e.g. balance-weighted rate = `SUM(rate*balance)/SUM(balance)`.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Total original lending: `SUM(original_amount)` across all loans, rounded to 0 dp.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Number of loans per `purpose`. Return `purpose`, `loans`; sorted by `loans` descending then `purpose`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Average original loan amount per `channel`, rounded to 0 dp. Return `channel`, `avg_amount`; sorted by `channel`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★ &nbsp; (warm-up)

Number of distinct primary customers with a loan. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q05 &nbsp; ★ &nbsp; (warm-up)

Smallest, largest and average `original_amount` for Active loans (average rounded to 0 dp). Three columns: min, max, avg.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q06 &nbsp; ★ &nbsp; (warm-up)

Loans per `loan_status`. Return `loan_status`, `loans`; sorted by `loan_status`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

For each origination year and `purpose`: number of loans. Return `yr`, `purpose`, `loans`; sorted by `yr`, `purpose`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **47 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

Which `product_id` values have more than 3,000 loans? Return `product_id`, `loans`; sorted by `product_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **9 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

Balance-weighted average interest rate on the latest snapshot (`snapshot_date = 2025-12-31`) for non-closed loans, as a single number rounded to 3 dp: `SUM(rate*balance)/SUM(balance)`. Use `closing_balance` and `interest_rate_pct`.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q10 &nbsp; ★★ &nbsp; (core)

Total outstanding balance at 2025-12-31 by `repayment_type` for non-closed loans. Return `repayment_type`, `balance` (0 dp); sorted by `repayment_type`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★ &nbsp; (core)

Approval rate by `channel` for applications that reached a decision: `Approved` count / decided count, as a % to 1 dp. Return `channel`, `approval_pct`; sorted by `channel`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★ &nbsp; (core)

Number of applications per `decline_reason_code` (declined only, code not null). Return `decline_reason_code`, `n`; sorted by `n` descending, then code.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★ &nbsp; (core)

Per `broker_id` (not NULL): number of loans and total original amount (0 dp). Show only brokers with at least 200 loans. Return `broker_id`, `loans`, `total_amount`; sorted by `total_amount` descending then `broker_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **30 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q14 &nbsp; ★★ &nbsp; (core)

Average LVR at origination per `purpose` (1 dp), excluding Internal Refinance. Return `purpose`, `avg_lvr`; sorted by `purpose`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★ &nbsp; (core)

Use `GROUP BY ALL`: count loans by `rate_type`, `loan_status`. Return `rate_type`, `loan_status`, `loans`; sorted by the first two.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★ &nbsp; (core)

One-row portfolio summary of Active loans at 2025-12-31 (snapshot table): `loan_count`, `total_balance` (0dp), `avg_balance` (0dp), `max_balance` (0dp).

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★★★ &nbsp; (challenge)

Conditional aggregation in one pass: for each `channel`, return counts of loans in each LVR bucket: `lvr_le80` (<= 80), `lvr_80_90` (> 80 and <= 90), `lvr_gt90` (> 90). Return `channel`, those three counts; sorted by `channel`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q18 &nbsp; ★★★ &nbsp; (challenge)

Arrears rate. At 2025-12-31, for non-closed loans: `loans`, `loans_30plus` (days_past_due >= 30), `loans_90plus` (>= 90), and the 90+ rate as % of balance (2 dp) = SUM(balance where dpd>=90)/SUM(balance)*100. Return the four values as one row: loans, loans_30plus, loans_90plus, pct_balance_90plus.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★★★ &nbsp; (challenge)

Median vs mean. For loans originated in 2025 compute, per `purpose`, the average and the median `original_amount` (both 0 dp). Return `purpose`, `avg_amount`, `median_amount`; sorted by `purpose`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q20 &nbsp; ★★★ &nbsp; (challenge)

Concentration: share of total Active-loan balance (snapshot 2025-12-31) held by each state of the property postcode. Join snapshot -> loan -> property -> dim_postcode. Return `state`, `balance_share_pct` (1 dp); sorted by share descending then `state`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q21 &nbsp; ★★★ &nbsp; (challenge)

Customers with the most loans. Return `primary_customer_id`, `loans` for customers with 4 or more loans as primary; sorted by `loans` descending then id. (Counts include closed and internal-refinance child loans.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1,100 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q22 &nbsp; ★★★ &nbsp; (challenge)

Fixed vs variable pricing check: per `rate_type` and origination year, the average `interest_rate_at_origination_pct` (2 dp). Return `rate_type`, `yr`, `avg_rate`; sorted by `rate_type`, `yr`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **16 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q23 &nbsp; ★★★ &nbsp; (challenge)

Spot the HAVING-vs-WHERE difference: states (from `customer.state` after UPPER/TRIM) where the share of customers with a NULL DOB exceeds 0.17% - return `state_clean`, `null_dob`, `customers`, `pct` (2dp) for those states, sorted by `state_clean`. Only keep rows where state_clean is a clean 2-3 letter code.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q24 &nbsp; ★ &nbsp; (warm-up)

For each purpose return the number of loans and the total original amount (0 dp). Return the purpose first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q25 &nbsp; ★ &nbsp; (warm-up)

For each purpose return the average original amount (0 dp) and the average origination LVR (1 dp). Return the purpose first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q26 &nbsp; ★ &nbsp; (warm-up)

For each purpose return the smallest and largest original amount. Return the purpose first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q27 &nbsp; ★★ &nbsp; (core)

For each purpose return the share of all loans (1 dp %) - hint: `COUNT(*)*100.0/SUM(COUNT(*)) OVER ()`. Return the purpose first; sorted by it.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q28 &nbsp; ★★ &nbsp; (core)

For each purpose return the average interest rate at origination (3 dp) and the average term in months (1 dp). Return the purpose first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q29 &nbsp; ★ &nbsp; (warm-up)

For each channel return the number of loans and the total original amount (0 dp). Return the channel first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q30 &nbsp; ★ &nbsp; (warm-up)

For each channel return the average original amount (0 dp) and the average origination LVR (1 dp). Return the channel first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q31 &nbsp; ★ &nbsp; (warm-up)

For each channel return the smallest and largest original amount. Return the channel first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q32 &nbsp; ★★ &nbsp; (core)

For each channel return the share of all loans (1 dp %) - hint: `COUNT(*)*100.0/SUM(COUNT(*)) OVER ()`. Return the channel first; sorted by it.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q33 &nbsp; ★★ &nbsp; (core)

For each channel return the average interest rate at origination (3 dp) and the average term in months (1 dp). Return the channel first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★ &nbsp; (warm-up)

For each rate_type return the number of loans and the total original amount (0 dp). Return the rate_type first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★ &nbsp; (warm-up)

For each rate_type return the average original amount (0 dp) and the average origination LVR (1 dp). Return the rate_type first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q36 &nbsp; ★ &nbsp; (warm-up)

For each rate_type return the smallest and largest original amount. Return the rate_type first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q37 &nbsp; ★★ &nbsp; (core)

For each rate_type return the share of all loans (1 dp %) - hint: `COUNT(*)*100.0/SUM(COUNT(*)) OVER ()`. Return the rate_type first; sorted by it.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q38 &nbsp; ★★ &nbsp; (core)

For each rate_type return the average interest rate at origination (3 dp) and the average term in months (1 dp). Return the rate_type first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q39 &nbsp; ★ &nbsp; (warm-up)

For each product_id return the number of loans and the total original amount (0 dp). Return the product_id first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q40 &nbsp; ★ &nbsp; (warm-up)

For each product_id return the average original amount (0 dp) and the average origination LVR (1 dp). Return the product_id first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q41 &nbsp; ★ &nbsp; (warm-up)

For each product_id return the smallest and largest original amount. Return the product_id first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q42 &nbsp; ★★ &nbsp; (core)

For each product_id return the share of all loans (1 dp %) - hint: `COUNT(*)*100.0/SUM(COUNT(*)) OVER ()`. Return the product_id first; sorted by it.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q43 &nbsp; ★★ &nbsp; (core)

For each product_id return the average interest rate at origination (3 dp) and the average term in months (1 dp). Return the product_id first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q44 &nbsp; ★ &nbsp; (warm-up)

For each origination year return the number of loans and the total original amount (0 dp). Return the origination year first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q45 &nbsp; ★ &nbsp; (warm-up)

For each origination year return the average original amount (0 dp) and the average origination LVR (1 dp). Return the origination year first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q46 &nbsp; ★ &nbsp; (warm-up)

For each origination year return the smallest and largest original amount. Return the origination year first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q47 &nbsp; ★★ &nbsp; (core)

For each origination year return the share of all loans (1 dp %) - hint: `COUNT(*)*100.0/SUM(COUNT(*)) OVER ()`. Return the origination year first; sorted by it.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q48 &nbsp; ★★ &nbsp; (core)

For each origination year return the average interest rate at origination (3 dp) and the average term in months (1 dp). Return the origination year first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q49 &nbsp; ★ &nbsp; (warm-up)

For each loan_status return the number of loans and the total original amount (0 dp). Return the loan_status first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q50 &nbsp; ★ &nbsp; (warm-up)

For each loan_status return the average original amount (0 dp) and the average origination LVR (1 dp). Return the loan_status first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q51 &nbsp; ★ &nbsp; (warm-up)

For each loan_status return the smallest and largest original amount. Return the loan_status first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q52 &nbsp; ★★ &nbsp; (core)

For each loan_status return the share of all loans (1 dp %) - hint: `COUNT(*)*100.0/SUM(COUNT(*)) OVER ()`. Return the loan_status first; sorted by it.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q53 &nbsp; ★★ &nbsp; (core)

For each loan_status return the average interest rate at origination (3 dp) and the average term in months (1 dp). Return the loan_status first; sorted by it.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q54 &nbsp; ★★ &nbsp; (core)

Origination years in which more than 2500 loans were written: `yr`, `loans`; sorted by year.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q55 &nbsp; ★★ &nbsp; (core)

Product ids with more than 1000 loans: `product_id`, `loans`; sorted by product_id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **14 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q56 &nbsp; ★★ &nbsp; (core)

Product ids with more than 2000 loans: `product_id`, `loans`; sorted by product_id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q57 &nbsp; ★★ &nbsp; (core)

For `'Broker'` loans: the count by purpose, with the % of the channel's loans (1 dp). `purpose`, `loans`, `pct`; sorted by `purpose`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q58 &nbsp; ★★ &nbsp; (core)

For `'Branch'` loans: the count by purpose, with the % of the channel's loans (1 dp). `purpose`, `loans`, `pct`; sorted by `purpose`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q59 &nbsp; ★★ &nbsp; (core)

For `'Digital'` loans: the count by purpose, with the % of the channel's loans (1 dp). `purpose`, `loans`, `pct`; sorted by `purpose`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q60 &nbsp; ★★ &nbsp; (core)

For `'Mobile Lender'` loans: the count by purpose, with the % of the channel's loans (1 dp). `purpose`, `loans`, `pct`; sorted by `purpose`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q61 &nbsp; ★★★ &nbsp; (challenge)

For 2021 originations: per `purpose` the count, total amount (0 dp), and the `COUNT(*) FILTER` of loans with LVR above 80. `purpose`, `loans`, `amount`, `lvr_gt80`; sorted by `purpose`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q62 &nbsp; ★★★ &nbsp; (challenge)

For 2023 originations: per `purpose` the count, total amount (0 dp), and the `COUNT(*) FILTER` of loans with LVR above 80. `purpose`, `loans`, `amount`, `lvr_gt80`; sorted by `purpose`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q63 &nbsp; ★★★ &nbsp; (challenge)

For 2025 originations: per `purpose` the count, total amount (0 dp), and the `COUNT(*) FILTER` of loans with LVR above 80. `purpose`, `loans`, `amount`, `lvr_gt80`; sorted by `purpose`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.
