# 07 - Merge, join and concat

`answers/07_merge/qNN.py` &nbsp;|&nbsp; check with: `grade 07` or `grade 07 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

**Read with:** McKinney ch 8 (combining and merging datasets).

## merge = SQL join

```
 loan                      dim_product                 loan.merge(dim_product, on='product_id', how='left')
 loan_id  product_id       product_id  occupancy       loan_id  product_id  occupancy
 1        3                3           Owner Occ       1        3           Owner Occ
 2        5                5           Investment      2        5           Investment
 3        99               (no 99)                     3        99          NaN        <- kept by 'left'
```

| how | keeps |
|---|---|
| `'inner'` (default) | only keys on both sides |
| `'left'` | every left row |
| `'outer'` | everything |

## Three habits that prevent silent bugs

1. **Check the row count** before and after. A many-to-one lookup must not add rows.
2. **`validate='many_to_one'`** makes pandas raise an error if the right side has duplicate keys.
3. **`indicator=True`** adds a `_merge` column (`left_only` / `right_only` / `both`): the easy anti-join.

## Fan-out
If the right side has 2 rows for one key, the left row appears twice. A loan with two securities becomes
two rows, and any sum of loan amounts after the join is now **double counted**.

## Other joins
- Different column names: `left_on='primary_customer_id', right_on='customer_id'`.
- Two keys: `on=['application_id', 'customer_id']`.
- "Value in force at a date": `pd.merge_asof(left.sort_values('d'), right.sort_values('d2'), left_on='d', right_on='d2')`
  takes the last right row at or before each left date.
- Stacking tables with the same columns: `pd.concat([a, b])`.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Bring `occupancy` from `dim_product` onto `loan` and count loans per occupancy. Return `occupancy`, `loans`;
sorted by `occupancy`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`, `dim_product`

### Q02 &nbsp; ★ &nbsp; (warm-up)

Join `app` to `assess` on `application_id` and return the median `nsr` for `'Approved'` and `'Declined'`
decisions, rounded to 3 dp. Return `decision`, `median_nsr`; sorted by `decision`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `app`, `assess`

### Q03 &nbsp; ★★ &nbsp; (core)

Anti-join: how many customers are **never** the `primary_customer_id` on a loan? (`indicator=True`)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `customer`, `loan`

### Q04 &nbsp; ★★ &nbsp; (core)

Fan-out check. Join `loan` to `loan_security` on `loan_id` (inner). Return one row: `rows_before` (loans),
`rows_after` (rows after the join) and `amount_double_counted` = the sum of `original_amount` after the join
minus the true total, rounded to 0 dp.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `loan`, `loan_security`

### Q05 &nbsp; ★★ &nbsp; (core)

Loans per **branch state** (join `dim_branch` on `branch_id` with `validate='many_to_one'`; loans with no branch
are left out). Return `state`, `loans`; sorted by `loans` (most first), then `state`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`, `dim_branch`

### Q06 &nbsp; ★★ &nbsp; (core)

The **primary** applicant's bureau score per application: join `applicant` (role `'Primary'`) to `bureau` on
**both** `application_id` and `customer_id`, then join `app` for the decision. Average `bureau_score` (thin files
excluded) per `decision`, rounded to 1 dp. Return `decision`, `avg_score`; sorted by `decision`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `applicant`, `bureau`, `app`

### Q07 &nbsp; ★★★ &nbsp; (challenge)

For each loan, find the **RBA cash rate in force** at its `origination_date` (latest `bank_effective_date` on or
before it, `merge_asof`). Average spread = `interest_rate_at_origination_pct` minus `cash_rate_pct`, per origination
year, rounded to 3 dp. Return `year`, `avg_spread`; sorted by `year`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`, `ref_rba_cash_rate`

<details><summary>hint</summary>

Both frames must be sorted by their date column before `merge_asof`.

</details>

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Arrears bucket for each live loan at 2025-12-31 using `ref_arrears_bucket` (`merge_asof` on `days_past_due`
against `dpd_from`). Return `bucket_name`, `loans` for every bucket that has loans; sorted by `bucket_id`
(so in bucket order, not alphabetical).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `ref_arrears_bucket`

<details><summary>hint</summary>

merge_asof needs both sides sorted, and int keys of the same type. Sort the result by bucket_id, then drop it.

</details>

### Q09 &nbsp; ★★ &nbsp; (core)

Stack two small tables with `pd.concat`: loans per channel originated in 2024 and in 2025, in **long** form.
Return `year`, `channel`, `loans`; sorted by `year`, `channel`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`
