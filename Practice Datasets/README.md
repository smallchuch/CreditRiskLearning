# Credit Risk Practice Datasets

Four linked, deliberately messy CSVs for pandas practice: cleaning, merging, groupby, and date/type handling.

## Files & relationships

- `borrowers.csv` — one row per borrower (`borrower_id`)
- `loans.csv` — one row per loan, links to `borrowers` via `borrower_id`
- `repayments.csv` — one row per payment, links to `loans` via `loan_id`
- `credit_bureau.csv` — one or more credit reports per borrower, links via `borrower_id`

Join path: `credit_bureau` → `borrowers` → `loans` → `repayments`

## Known issues (seeded on purpose)

**borrowers.csv**
- Missing values in `annual_income`, `employment_status`, `credit_score`
- Inconsistent casing: `Employed` / `employed` / `EMPLOYED` / `Self-Employed` / `self-employed`
- `state` mixes abbreviations and full names (`CA` vs `California`)
- Exact duplicate row (`B003` appears twice, one with extra whitespace)
- Invalid ages (`-5`, `151`), invalid credit scores (`999`, `0`)
- Leading/trailing whitespace in some names

**loans.csv**
- Mixed date formats in `issue_date` (`2023-01-15`, `01/22/2023`, `15-Feb-2023`, `2023/03/01`)
- `interest_rate` sometimes a string with `%`, sometimes a plain number
- `status` and `purpose` inconsistent casing/spacing (`Current`/`current`/`DEFAULT`, `credit_card`/`Credit Card`)
- Missing `loan_amount` and `interest_rate` values
- One negative `loan_amount` (data entry error)
- One loan references a `borrower_id` (`B999`) not present in `borrowers.csv`, and one borrower (`B041`) in loans doesn't exist either — good for testing merge behavior (`how="left"` vs `"inner"`)

**repayments.csv**
- Mixed date formats in `payment_date`
- Missing `amount_paid`
- Negative `amount_paid` (refunds/errors)
- `payment_method` inconsistent casing (`ACH`/`ach`, `Check`/`check`, `Wire`/`wire transfer`)
- Negative `days_late` (paid early, encoded oddly)
- Duplicate payment (`L1001` billed for the same period twice)
- One payment references a `loan_id` (`L9999`) not present in `loans.csv`

**credit_bureau.csv**
- Some borrowers have two reports (different `report_date`) with different values
- `total_debt` sometimes formatted as `"$12,500"` (string with $ and comma), sometimes a plain number
- `bankruptcy_flag` inconsistent encoding: `Y`/`N`, `Yes`/`No`, `1`/`0`
- Missing `num_open_accounts` and `total_debt` values

## Suggested exercises

Load each file and check dtypes and nulls. Standardize `employment_status`, `purpose`, `status`, and `payment_method` to a consistent casing. Parse all date columns with mixed formats using `pd.to_datetime(..., format='mixed')` or per-format parsing. Strip `$`/`,` from `loan_amount`, `total_debt`, and `%` from `interest_rate`, then cast to numeric. Drop or flag the exact duplicate borrower and the duplicate payment. Normalize `bankruptcy_flag` to boolean. Merge `borrowers` → `loans` → `repayments` and decide how to handle the orphaned `B999`/`L9999` records. Compute per-borrower total paid, total late fees exposure, and default rate by loan purpose or state.
