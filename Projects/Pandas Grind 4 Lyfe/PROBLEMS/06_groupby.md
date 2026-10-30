# 06 - GroupBy: aggregate, transform, filter

`answers/06_groupby/qNN.py` &nbsp;|&nbsp; check with: `grade 06` or `grade 06 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

**Read with:** McKinney ch 10 (GroupBy mechanics, aggregation, apply / transform).

## split -> apply -> combine

```
 loan rows                   split by channel          apply mean         combine
 channel  amount             Branch: 400k, 600k  ->     500k              channel  mean
 Branch   400k               Broker: 300k        ->     300k              Branch   500k
 Broker   300k                                                            Broker   300k
 Branch   600k
```
The group keys end up in the **index** of the result. `.reset_index()` (or `as_index=False`) turns them into columns.

## The four shapes of aggregation

| Write | Get |
|---|---|
| `df.groupby('k')['x'].mean()` | Series, one number per group |
| `df.groupby('k').size()` | rows per group (counts missing too) |
| `df.groupby('k')['x'].count()` | non-missing `x` per group |
| `df.groupby('k').agg(loans=('x', 'size'), avg=('x', 'mean'))` | named columns: the tidy way |

## transform: a group number on every row

```
 channel  amount   mean by channel (transform)   amount - mean
 Branch   400k     500k                          -100k
 Branch   600k     500k                          +100k
 Broker   300k     300k                             0
```
`df.groupby('k')['x'].transform('mean')` keeps the original row count, so you can compare each row with its group.

## Weighted average (credit risk staple)
`(x * w).sum() / w.sum()` per group. In a groupby, build `x * w` as a column first, then sum both and divide.

## Other everyday moves
`.filter(lambda g: len(g) > 200)` keeps whole groups; `.nlargest`, `.idxmax()` find the top row;
`sort_values(...).groupby(...).head(1)` = top row per group.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Number of loans per `purpose`. Return `purpose`, `loans`; sorted by `loans` (most first), then `purpose`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q02 &nbsp; ★ &nbsp; (warm-up)

Average `original_amount` per `channel`, rounded to 0 dp. Return `channel`, `avg_amount`; sorted by `channel`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q03 &nbsp; ★ &nbsp; (warm-up)

Per `rate_type`, with named aggregation: `loans` (count), `total_amount` (sum of `original_amount`, rounded to 0 dp)
and `avg_lvr` (mean `lvr_at_origination_pct`, rounded to 2 dp). Return `rate_type`, `loans`, `total_amount`, `avg_lvr`;
sorted by `rate_type`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q04 &nbsp; ★★ &nbsp; (core)

Live book at 2025-12-31 (`snapshot_date` = 2025-12-31, `loan_status` not `'Closed'`): the **balance-weighted**
average `interest_rate_pct` per `repayment_type`, rounded to 3 dp. Return `repayment_type`, `wavg_rate`; sorted by `repayment_type`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`

### Q05 &nbsp; ★★ &nbsp; (core)

Loans per origination year and `rate_type`. Return `year`, `rate_type`, `loans`; sorted by `year`, `rate_type`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **16 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q06 &nbsp; ★★ &nbsp; (core)

For each loan, compare `original_amount` with the **average for its channel** (`transform`). Per channel, how many
loans are above their channel average? Return `channel`, `above_avg`; sorted by `channel`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q07 &nbsp; ★★ &nbsp; (core)

Brokers (`broker_id`, broker-channel loans) that wrote **more than 250** loans. Return `broker_id` (as an int),
`loans`; sorted by `loans` (most first), then `broker_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **23 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q08 &nbsp; ★★ &nbsp; (core)

`size()` vs `count()`: per channel, the number of rows and the number with a `branch_id`. Return `channel`, `rows`,
`with_branch`; sorted by `channel`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q09 &nbsp; ★★★ &nbsp; (challenge)

The single largest loan in each `purpose` (ties: smaller `loan_id` wins). Return `purpose`, `loan_id`,
`original_amount`; sorted by `purpose`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

<details><summary>hint</summary>

Sort first, then `groupby(...).head(1)` keeps the first row of each group.

</details>

### Q10 &nbsp; ★★★ &nbsp; (challenge)

On `app`, among applications that have a `decision`, the approval rate per `channel` as a percentage
rounded to 2 dp. Return `channel`, `approval_pct`; sorted by `channel`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `app`
