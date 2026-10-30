from . import P

PRIMER = r"""
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
"""

CONCEPT = dict(id="01_python_basics", title="01 - Python basics: types, f-strings, lists, dicts, loops", primer=PRIMER, problems=[
    P(1, """
Total original lending across all loans, as a **string** formatted like `$12,345,678` (dollar sign, thousands
commas, no decimals). Return the string.
""", """
total = loan['original_amount'].sum()
result = f"${total:,.0f}"
""", ["loan"], hint="Format specs go inside an f-string: `f\"{x:,.0f}\"`. A float has no `.format` method."),

    P(1, """
The distinct `channel` values on `loan`, in alphabetical order, as a plain Python **list**.
""", """
result = sorted(loan['channel'].unique())
""", ["loan"], order=True),

    P(1, """
A **dict** mapping `product_id` to `product_name` for every product. Return the dict (it is graded as key, value pairs).
""", """
result = dict(zip(dim_product['product_id'], dim_product['product_name']))
""", ["dim_product"], hint="`dict(zip(keys, values))` builds a dict from two columns."),

    P(1, """
The number of loans originated in each calendar year, as a dict `{year: loans}` built **with a loop**
(no groupby). Years are ints.
""", """
counts = {}
for y in loan['origination_date'].dt.year:
    counts[int(y)] = counts.get(int(y), 0) + 1
result = counts
""", ["loan"], hint="`d.get(key, 0) + 1` is the classic counting idiom. (`value_counts` would do it in one line, but practise the loop.)"),

    P(2, """
Rank the channels by number of loans (most first) and return a **list of strings** like `'1. Broker (35,570)'`.
""", """
counts = loan['channel'].value_counts()
result = [f"{i}. {name} ({n:,})" for i, (name, n) in enumerate(counts.items(), start=1)]
""", ["loan"], order=True, hint="`enumerate(series.items(), start=1)` gives `i, (label, value)`."),

    P(2, """
Each rule below is `name: (column, threshold)`. Loop over the dict and count the loans where the column is
**strictly above** the threshold. Return `rule`, `loans`; sorted by `rule`.

```python
rules = {
    'big_loan':  ('original_amount', 1_000_000),
    'high_lvr':  ('lvr_at_origination_pct', 90),
    'high_rate': ('interest_rate_at_origination_pct', 7),
}
```
""", """
rules = {
    'big_loan':  ('original_amount', 1_000_000),
    'high_lvr':  ('lvr_at_origination_pct', 90),
    'high_rate': ('interest_rate_at_origination_pct', 7),
}
counts = {}
for name, (col, cut) in rules.items():
    counts[name] = int((loan[col] > cut).sum())
result = pd.Series(counts, name='loans').rename_axis('rule').sort_index()
""", ["loan"], hint="`for name, (col, cut) in rules.items():` unpacks the tuple. A True/False Series `.sum()` counts the Trues."),

    P(2, """
Write a function `pct_above(series, cut)` that returns the **percentage** of values strictly above `cut`
(ignore missing values in the denominator). Use it for `lvr_at_origination_pct` at cuts 60, 70, 80, 90 and 95.
Return `cut`, `pct` (rounded to 2 dp); sorted by `cut`.
""", """
def pct_above(series, cut):
    s = series.dropna()
    return 100 * (s > cut).mean()

result = pd.DataFrame({'cut': [60, 70, 80, 90, 95]})
result['pct'] = [round(pct_above(loan['lvr_at_origination_pct'], c), 2) for c in result['cut']]
""", ["loan"], hint="The mean of a True/False Series is the share of Trues."),

    P(3, """
Build a nested dict `{purpose: {'loans': n, 'avg_amount': mean}}` with a loop over the purposes, then turn it
into a table. Return `purpose`, `loans`, `avg_amount` (rounded to 0 dp); sorted by `purpose`.
""", """
summary = {}
for purpose in sorted(loan['purpose'].unique()):
    amounts = loan.loc[loan['purpose'] == purpose, 'original_amount']
    summary[purpose] = {'loans': len(amounts), 'avg_amount': round(amounts.mean(), 0)}
result = pd.DataFrame(summary).T.rename_axis('purpose').reset_index()
""", ["loan"], hint="`pd.DataFrame(nested_dict)` puts the outer keys as columns, so `.T` flips them into rows."),
])
