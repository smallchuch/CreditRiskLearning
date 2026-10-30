# 05 - Missing values, dtypes, strings and duplicates

`answers/05_missing_strings/qNN.py` &nbsp;|&nbsp; check with: `grade 05` or `grade 05 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

**Read with:** McKinney ch 7 (missing data, string methods, data transformation, duplicates).

## Missing values: know how each tool treats them

| Tool | Missing values |
|---|---|
| `s.mean()`, `s.sum()`, `s.count()` | skipped |
| `len(s)`, `s.size` | counted |
| `s.isna()` / `s.notna()` | True / False per row |
| `s.fillna(0)` | replaced (careful: **changes the mean**) |
| `s.fillna(other_series)` | filled row by row from another column (aligned by label) |
| `df.dropna(subset=['col'])` | rows dropped |

A thin-file bureau score is **missing, not zero**. Filling it with 0 drags the average down and calls a
no-history applicant a terrible one.

## String cleaning: chain the `.str` methods

```python
s.str.strip().str.upper()                     # ' sa ' -> 'SA'
s.str.replace('.', '', regex=False)           # 'S.A.' -> 'SA'
s.str.replace(r'\s+', '', regex=True)         # remove all whitespace
s.str.startswith('+61')
s.str.len()
s.replace({'SOUTH AUSTRALIA': 'SA'})          # whole-value mapping
```

## Duplicates

```python
key = [first.str.strip().str.lower(), last.str.strip().str.lower(), dob]
df.duplicated(subset=[...])            # True for the 2nd, 3rd ... copy
df.duplicated(subset=[...], keep=False) # True for every copy
```

## Sentinels and unit slips
A value that is technically valid but means something else (`365243` days employed, a rate keyed as
`0.0629` instead of `6.29`). Find it with a range check, fix it with a mask:
`df.loc[mask, 'col'] = df.loc[mask, 'col'] * 100`.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Which columns of `loan` have missing values, and how many? Return `column`, `n_missing` for columns with at
least one missing value; sorted by `column`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **9 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q02 &nbsp; ★ &nbsp; (warm-up)

How many bureau reports are thin files (missing `bureau_score`)?

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `bureau`

### Q03 &nbsp; ★ &nbsp; (warm-up)

The thin-file trap. Return two numbers in one row: the mean `bureau_score` **ignoring** thin files, and the
mean if thin files were (wrongly) filled with 0. Both rounded to 1 dp; columns `mean_skip`, `mean_zero`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `bureau`

### Q04 &nbsp; ★★ &nbsp; (core)

`customer['state']` is written many ways (`'S.A.'`, `'sa'`, `'South Australia'`, `'ACT '` ...). Clean it to the
eight codes `ACT NSW NT QLD SA TAS VIC WA` and count customers per state. Return `state`, `customers`; sorted by `state`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `customer`

<details><summary>hint</summary>

strip, upper-case, drop the dots, then map the full names. `s.unique()` shows what is left to fix.

</details>

### Q05 &nbsp; ★★ &nbsp; (core)

Each customer's age in **whole years** (rounded down) at 2025-12-31, from `date_of_birth`. Customers without a
date of birth are left out. Return the average age, rounded to 1 dp.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `customer`

<details><summary>hint</summary>

Year difference, minus 1 if the birthday hasn't happened yet that year. (At 31 December every birthday has happened, but write it properly anyway.)

</details>

### Q06 &nbsp; ★★ &nbsp; (core)

On `applicant_income`, use the verified amount where there is one and the declared amount otherwise
(`fillna` from another column). Return the total annual income across all lines, rounded to 0 dp.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `applicant_income`

### Q07 &nbsp; ★★ &nbsp; (core)

Duplicate customers: the same person (first name, last name and date of birth, ignoring case and spaces)
under more than one `customer_id`. Customers with no date of birth are left out. How many **extra** records
are there (rows minus distinct people)?

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `customer`

<details><summary>hint</summary>

`.duplicated()` marks every copy after the first, so its sum is exactly the number of extras.

</details>

### Q08 &nbsp; ★★ &nbsp; (core)

Mobile numbers come in mixed formats (`'0412345678'`, `'+61 412 345 678'`, `'0412 345 678'` ...). Normalise each
to 10 digits starting `04` (remove spaces, turn a leading `+61` into `0`). How many customers' numbers were
**not** already in that clean form?

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `customer`

### Q09 &nbsp; ★★★ &nbsp; (challenge)

A few `loan_rate_history` rates were keyed as fractions (`0.0629` instead of `6.29`). Find them (rate below 1),
fix them by multiplying by 100, and return one row: `n_fixed`, `mean_before`, `mean_after` (means rounded to 4 dp).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `loan_rate_history`
