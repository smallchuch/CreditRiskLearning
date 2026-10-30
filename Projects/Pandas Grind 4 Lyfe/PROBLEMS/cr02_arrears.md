# cr02 - Arrears, roll rates and cures

`answers/cr02_arrears/qNN.py` &nbsp;|&nbsp; check with: `grade cr02` or `grade cr02 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

**Credit-risk scenario.** Arrears, roll rates, cures and a first cohort default rate. Patterns from sets 06, 07, 08, 11.

## Arrears rate: count or balance?
```
 30+ rate (count)   = loans with dpd >= 30 / live loans
 30+ rate (balance) = balance of loans with dpd >= 30 / live balance     <- what APRA-style reporting uses
```

## Roll-rate matrix (this month's bucket given last month's)

```
                 Dec: Current  1-29  30-59  60-89  90+
 Nov: Current        99.3%     0.6%  0.1%    -      -        each ROW sums to 100%
      1-29           40%       35%   25%     -      -        diagonal = stayed
      30-59          15%       10%   20%    55%     -        right of diagonal = rolled forward
      ...                                                     left = cured
```
Build it: one row per loan with `bucket_nov` and `bucket_dec` (a merge of two snapshots), then
`pd.crosstab(bucket_nov, bucket_dec, normalize='index')`.

Use **ordered** labels so rows and columns come out in bucket order, not alphabetical:
```python
order = ['Current', '1-29', '30-59', '60-89', '90+']
b = pd.Categorical(labels, categories=order, ordered=True)
```

## Cohort default rate (a 12-month PD, the simple way)
Take a cohort at a start date (e.g. performing loans at 2024-12-31), follow them for 12 months, count who hit 90+.
Denominator = cohort size at the start. That's the shape of the PD your Freddie Mac project builds.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

The **30+ arrears rate by count** of the live book at each month-end of 2025 (live = not `'Closed'` that month),
as a percentage rounded to 3 dp. Month as `'2025-01'` etc. Return `month`, `pct_30plus`; sorted by `month`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`

### Q02 &nbsp; ★★ &nbsp; (core)

The **90+ arrears rate by balance** of the live book at 2025-12-31, as a percentage rounded to 3 dp.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`

### Q03 &nbsp; ★★ &nbsp; (core)

Live loans and balance by arrears bucket at 2025-12-31 with buckets `'Current'` (0), `'1-29'`, `'30-59'`, `'60-89'`,
`'90+'`. Return `bucket`, `loans`, `balance_m` (2 dp) in bucket order.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`

### Q04 &nbsp; ★★★ &nbsp; (challenge)

Roll-rate matrix November -> December 2025 for loans that are live (not `'Closed'`) in **both** month-end snapshots.
Buckets `Current`, `1-29`, `30-59`, `60-89`, `90+`; **row percentages** rounded to 2 dp,
0 where nothing rolled. Return `from_bucket` then one column per December bucket in bucket order; rows in bucket order.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`

### Q05 &nbsp; ★★ &nbsp; (core)

Cure rate: of the loans 30+ days past due at 2025-06-30, what percentage were back to 0 days past due at 2025-12-31?
Denominator = those 30+ at June that still have a December snapshot. Round to 2 dp.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`

### Q06 &nbsp; ★★ &nbsp; (core)

Share of live loans on a hardship flag at each **quarter-end of 2020** (the COVID deferral wave), as a percentage
rounded to 2 dp. Return `quarter_end` (`'2020-03-31'` etc.), `hardship_pct`; sorted by `quarter_end`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`

### Q07 &nbsp; ★★★ &nbsp; (challenge)

A 12-month cohort default rate. Cohort = live loans at 2024-12-31 that were **current** (0 days past due) then.
Bad = reached 90+ days past due at **any** 2025 month-end. Return one row: `cohort`, `bads`, `default_rate_pct` (3 dp).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`
