# 01 - Python basics: types, f-strings, lists, dicts, loops

`answers/01_python_basics/qNN.py` &nbsp;|&nbsp; check with: `grade 01` or `grade 01 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

**Read with:** McKinney ch 2 (types, methods, "everything is an object") and ch 3 (list, dict, tuple, comprehensions).

## Every value has a type, and the type decides what you can call on it

```
 value                    type          some methods / tools
 1234.5                   float         round(x, 2)   f"{x:,.2f}"      (no .format!)
 "Broker"                 str           .upper()  .startswith()  "{:.2f}".format(x)
 [3, 1, 2]                list          .append()  sorted()  len()
 {"a": 1}                 dict          .items()  .keys()  d["a"]
 loan["original_amount"]  pd.Series     .mean()  .sum()  .value_counts()
```
When Python says `AttributeError: 'float' object has no attribute 'format'`, it is telling you the
method belongs to a different type. Check with `type(x)`.

## f-strings: the one formatting tool you need

| You write | You get |
|---|---|
| `f"{x:.2f}"` | `1234.57` |
| `f"{x:,.0f}"` | `1,235` |
| `f"{p:.1%}"` | `8.1%` (p = 0.0807) |
| `f"{name}: {n:,}"` | `Broker: 35,570` |

## Loops you will use constantly

```python
for i, name in enumerate(names, start=1): ...        # position + item
for a, b in zip(list_a, list_b): ...                 # walk two lists together
for key, value in d.items(): ...                     # walk a dict
for name, (col, cut) in rules.items(): ...           # unpack a tuple inside the loop
[x * 2 for x in nums if x > 0]                       # list comprehension
{k: v for k, v in pairs}                             # dict comprehension
```

**Pattern to remember:** collect results in a dict inside a loop, then turn it into a table once at the end.
```python
rows = {}
for name, thing in things.items():
    rows[name] = some_number(thing)
pd.Series(rows)          # or pd.DataFrame(rows).T for several numbers per name
```

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Total original lending across all loans, as a **string** formatted like `$12,345,678` (dollar sign, thousands
commas, no decimals). Return the string.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `loan`

<details><summary>hint</summary>

Format specs go inside an f-string: `f"{x:,.0f}"`. A float has no `.format` method.

</details>

### Q02 &nbsp; ★ &nbsp; (warm-up)

The distinct `channel` values on `loan`, in alphabetical order, as a plain Python **list**.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q03 &nbsp; ★ &nbsp; (warm-up)

A **dict** mapping `product_id` to `product_name` for every product. Return the dict (it is graded as key, value pairs).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `dim_product`

<details><summary>hint</summary>

`dict(zip(keys, values))` builds a dict from two columns.

</details>

### Q04 &nbsp; ★ &nbsp; (warm-up)

The number of loans originated in each calendar year, as a dict `{year: loans}` built **with a loop**
(no groupby). Years are ints.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `loan`

<details><summary>hint</summary>

`d.get(key, 0) + 1` is the classic counting idiom. (`value_counts` would do it in one line, but practise the loop.)

</details>

### Q05 &nbsp; ★★ &nbsp; (core)

Rank the channels by number of loans (most first) and return a **list of strings** like `'1. Broker (35,570)'`.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

<details><summary>hint</summary>

`enumerate(series.items(), start=1)` gives `i, (label, value)`.

</details>

### Q06 &nbsp; ★★ &nbsp; (core)

Each rule below is `name: (column, threshold)`. Loop over the dict and count the loans where the column is
**strictly above** the threshold. Return `rule`, `loans`; sorted by `rule`.

```python
rules = {
    'big_loan':  ('original_amount', 1_000_000),
    'high_lvr':  ('lvr_at_origination_pct', 90),
    'high_rate': ('interest_rate_at_origination_pct', 7),
}
```

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

<details><summary>hint</summary>

`for name, (col, cut) in rules.items():` unpacks the tuple. A True/False Series `.sum()` counts the Trues.

</details>

### Q07 &nbsp; ★★ &nbsp; (core)

Write a function `pct_above(series, cut)` that returns the **percentage** of values strictly above `cut`
(ignore missing values in the denominator). Use it for `lvr_at_origination_pct` at cuts 60, 70, 80, 90 and 95.
Return `cut`, `pct` (rounded to 2 dp); sorted by `cut`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

<details><summary>hint</summary>

The mean of a True/False Series is the share of Trues.

</details>

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Build a nested dict `{purpose: {'loans': n, 'avg_amount': mean}}` with a loop over the purposes, then turn it
into a table. Return `purpose`, `loans`, `avg_amount` (rounded to 0 dp); sorted by `purpose`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

<details><summary>hint</summary>

`pd.DataFrame(nested_dict)` puts the outer keys as columns, so `.T` flips them into rows.

</details>
