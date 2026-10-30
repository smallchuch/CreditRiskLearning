from . import P

PRIMER = r"""
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
"""

STATE_FIX = """
s = customer['state'].str.strip().str.upper().str.replace('.', '', regex=False)
full = {'SOUTH AUSTRALIA': 'SA', 'VICTORIA': 'VIC', 'NEW SOUTH WALES': 'NSW', 'QUEENSLAND': 'QLD',
        'WESTERN AUSTRALIA': 'WA', 'TASMANIA': 'TAS', 'NORTHERN TERRITORY': 'NT'}
s = s.replace(full)
"""

CONCEPT = dict(id="05_missing_strings", title="05 - Missing values, dtypes, strings and duplicates", primer=PRIMER, problems=[
    P(1, """
Which columns of `loan` have missing values, and how many? Return `column`, `n_missing` for columns with at
least one missing value; sorted by `column`.
""", """
n = loan.isna().sum()
result = n[n > 0].rename_axis('column').sort_index()
""", ["loan"]),

    P(1, """
How many bureau reports are thin files (missing `bureau_score`)?
""", """
result = int(bureau['bureau_score'].isna().sum())
""", ["credit_bureau_report"]),

    P(1, """
The thin-file trap. Return two numbers in one row: the mean `bureau_score` **ignoring** thin files, and the
mean if thin files were (wrongly) filled with 0. Both rounded to 1 dp; columns `mean_skip`, `mean_zero`.
""", """
s = bureau['bureau_score']
result = pd.DataFrame({'mean_skip': [round(s.mean(), 1)], 'mean_zero': [round(s.fillna(0).mean(), 1)]})
""", ["credit_bureau_report"]),

    P(2, """
`customer['state']` is written many ways (`'S.A.'`, `'sa'`, `'South Australia'`, `'ACT '` ...). Clean it to the
eight codes `ACT NSW NT QLD SA TAS VIC WA` and count customers per state. Return `state`, `customers`; sorted by `state`.
""", STATE_FIX + """
result = s.value_counts().rename_axis('state').sort_index()
""", ["customer"], hint="strip, upper-case, drop the dots, then map the full names. `s.unique()` shows what is left to fix."),

    P(2, """
Each customer's age in **whole years** (rounded down) at 2025-12-31, from `date_of_birth`. Customers without a
date of birth are left out. Return the average age, rounded to 1 dp.
""", """
asat = pd.Timestamp('2025-12-31')
dob = customer['date_of_birth'].dropna()
age = asat.year - dob.dt.year - (dob.dt.strftime('%m%d') > asat.strftime('%m%d')).astype(int)
result = round(age.mean(), 1)
""", ["customer"], hint="Year difference, minus 1 if the birthday hasn't happened yet that year. (At 31 December every birthday has happened, but write it properly anyway.)"),

    P(2, """
On `applicant_income`, use the verified amount where there is one and the declared amount otherwise
(`fillna` from another column). Return the total annual income across all lines, rounded to 0 dp.
""", """
amount = applicant_income['verified_annual_amount'].fillna(applicant_income['declared_annual_amount'])
result = round(amount.sum(), 0)
""", ["applicant_income"]),

    P(2, """
Duplicate customers: the same person (first name, last name and date of birth, ignoring case and spaces)
under more than one `customer_id`. Customers with no date of birth are left out. How many **extra** records
are there (rows minus distinct people)?
""", """
c = customer.dropna(subset=['date_of_birth'])
key = pd.DataFrame({'f': c['first_name'].str.strip().str.lower(),
                    'l': c['last_name'].str.strip().str.lower(),
                    'd': c['date_of_birth']})
result = int(key.duplicated().sum())
""", ["customer"], hint="`.duplicated()` marks every copy after the first, so its sum is exactly the number of extras."),

    P(2, """
Mobile numbers come in mixed formats (`'0412345678'`, `'+61 412 345 678'`, `'0412 345 678'` ...). Normalise each
to 10 digits starting `04` (remove spaces, turn a leading `+61` into `0`). How many customers' numbers were
**not** already in that clean form?
""", """
m = customer['mobile']
clean = m.str.replace(r'\\s+', '', regex=True).str.replace(r'^\\+61', '0', regex=True)
result = int((m != clean).sum())
""", ["customer"]),

    P(3, """
A few `loan_rate_history` rates were keyed as fractions (`0.0629` instead of `6.29`). Find them (rate below 1),
fix them by multiplying by 100, and return one row: `n_fixed`, `mean_before`, `mean_after` (means rounded to 4 dp).
""", """
r = loan_rate_history['interest_rate_pct'].copy()
bad = r < 1
before = r.mean()
r[bad] = r[bad] * 100
result = pd.DataFrame({'n_fixed': [int(bad.sum())], 'mean_before': [round(before, 4)], 'mean_after': [round(r.mean(), 4)]})
""", ["loan_rate_history"], tol=0.00011),
])
