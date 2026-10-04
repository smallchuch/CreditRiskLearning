# CR10 - Reconciliations and control testing

`answers/cr10_reconciliation_controls/qNN.sql` &nbsp;|&nbsp; check with: `grade cr10` or `grade cr10 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Scenario: audit season - prove the numbers tie

Big 4 advisory / internal audit / model validation all ask the same thing: *"do these two sources agree, and if not, why?"*
This set is a series of **reconciliations and control tests**. Every query returns a count of breaks (ideally 0) or a table of differences.

```
 Source A total   vs   Source B total   ->   difference   ->   which records explain it?
```
Techniques: aggregate both sides to the same grain, `FULL OUTER JOIN` on the key, compare, `COALESCE(a,0) - COALESCE(b,0)`, list the breaks.

Tolerance: money to the cent is rarely exact after rounding - use a threshold (`ABS(diff) > 1`) and say so.
Known quirks are planted in this data; some "breaks" here are real data problems you should be able to explain.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Loan count tie-out: loans on `loan` vs distinct loans in `loan_monthly_snapshot` vs distinct loans in `loan_borrower`. `loan`, `snapshot`, `borrower`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Every loan has exactly one 'Primary' borrower on `loan_borrower`? Count loans with a primary-borrower count different from 1. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q03 &nbsp; ★ &nbsp; (warm-up)

`loan.primary_customer_id` agrees with the 'Primary' row in `loan_borrower`? Count mismatches. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q04 &nbsp; ★★ &nbsp; (core)

Origination vs first snapshot: loans where the first snapshot balance (`months_on_book = 0`) differs from `original_amount` by more than $1. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q05 &nbsp; ★★ &nbsp; (core)

Closed-loan control: loans closed on `loan` but still with an 'Active' or 'In Recovery' snapshot AFTER the closed date. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q06 &nbsp; ★★ &nbsp; (core)

ECL population vs live book: loans in the live book at 2025-12-31 but missing from `ecl_provision_quarterly` at that date, and ECL rows for loans NOT live. `live_not_in_ecl`, `ecl_not_live`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q07 &nbsp; ★★ &nbsp; (core)

EAD vs balance by loan: loans where `ecl_provision_quarterly.ead` at 2025-12-31 differs from the snapshot `closing_balance` by more than $100. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Payments vs snapshot: for 2025-12 (payments with `payment_date` in December 2025, status Paid), total paid (0dp) vs total `actual_repayment` in the 2025-12-31 snapshot (0dp) for non-closed loans. `payments`, `snapshot_actual`, `difference`. (Do they reconcile? What might explain a gap?)

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q09 &nbsp; ★★★ &nbsp; (challenge)

FULL OUTER JOIN reconciliation: loan counts by purpose in `loan` vs count of applications that settled (`current_status='Settled'`) by purpose in `loan_application`. Show `purpose`, `loans`, `settled_apps`, `diff`; sorted by purpose. (Internal refinance loans have no application.)

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★★ &nbsp; (challenge)

Loans to settled applications: settled applications with no loan, and loans with an `application_id` that point to a non-settled application. `settled_no_loan`, `loan_bad_app`. Both expected 0.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Rate history completeness: loans whose current snapshot rate (2025-12-31, non-closed) differs from the `loan_rate_history` row in force at that date by more than 0.01 percentage points (ignore rows keyed as fractions < 1). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Hardship flag vs hardship table: snapshots (live) at 2025-12-31 with `hardship_flag` true but no active hardship arrangement covering that date (`start_date <= date <= COALESCE(end_date, 9999)`). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q13 &nbsp; ★★ &nbsp; (core)

Year-end 2019: live loans in the snapshot vs rows in `ecl_provision_quarterly` at 2019-12-31, and the difference. `snapshot_live`, `ecl_rows`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★★ &nbsp; (core)

Year-end 2020: live loans in the snapshot vs rows in `ecl_provision_quarterly` at 2020-12-31, and the difference. `snapshot_live`, `ecl_rows`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q15 &nbsp; ★★ &nbsp; (core)

Year-end 2021: live loans in the snapshot vs rows in `ecl_provision_quarterly` at 2021-12-31, and the difference. `snapshot_live`, `ecl_rows`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q16 &nbsp; ★★ &nbsp; (core)

Year-end 2022: live loans in the snapshot vs rows in `ecl_provision_quarterly` at 2022-12-31, and the difference. `snapshot_live`, `ecl_rows`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★★ &nbsp; (core)

Year-end 2023: live loans in the snapshot vs rows in `ecl_provision_quarterly` at 2023-12-31, and the difference. `snapshot_live`, `ecl_rows`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★ &nbsp; (core)

Year-end 2024: live loans in the snapshot vs rows in `ecl_provision_quarterly` at 2024-12-31, and the difference. `snapshot_live`, `ecl_rows`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★★ &nbsp; (core)

Year-end 2025: live loans in the snapshot vs rows in `ecl_provision_quarterly` at 2025-12-31, and the difference. `snapshot_live`, `ecl_rows`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★★ &nbsp; (core)

Origination tie-out 2019: loans originated in 2019 per `loan` vs loans whose first snapshot (`months_on_book = 0`) is in 2019, and the difference. `loans`, `first_snapshots`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★ &nbsp; (core)

Origination tie-out 2020: loans originated in 2020 per `loan` vs loans whose first snapshot (`months_on_book = 0`) is in 2020, and the difference. `loans`, `first_snapshots`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★ &nbsp; (core)

Origination tie-out 2021: loans originated in 2021 per `loan` vs loans whose first snapshot (`months_on_book = 0`) is in 2021, and the difference. `loans`, `first_snapshots`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★ &nbsp; (core)

Origination tie-out 2022: loans originated in 2022 per `loan` vs loans whose first snapshot (`months_on_book = 0`) is in 2022, and the difference. `loans`, `first_snapshots`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★★ &nbsp; (core)

Origination tie-out 2023: loans originated in 2023 per `loan` vs loans whose first snapshot (`months_on_book = 0`) is in 2023, and the difference. `loans`, `first_snapshots`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★★ &nbsp; (core)

Origination tie-out 2024: loans originated in 2024 per `loan` vs loans whose first snapshot (`months_on_book = 0`) is in 2024, and the difference. `loans`, `first_snapshots`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★★ &nbsp; (core)

Origination tie-out 2025: loans originated in 2025 per `loan` vs loans whose first snapshot (`months_on_book = 0`) is in 2025, and the difference. `loans`, `first_snapshots`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★★★ &nbsp; (challenge)

Closure tie-out 2019: loans with `closed_date` in 2019 vs loans whose snapshot status first turns 'Closed' in 2019 (first `snapshot_date` with `loan_status='Closed'`), and the difference. `closed_loans`, `snapshot_closed`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★★★ &nbsp; (challenge)

Closure tie-out 2020: loans with `closed_date` in 2020 vs loans whose snapshot status first turns 'Closed' in 2020 (first `snapshot_date` with `loan_status='Closed'`), and the difference. `closed_loans`, `snapshot_closed`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★★★ &nbsp; (challenge)

Closure tie-out 2021: loans with `closed_date` in 2021 vs loans whose snapshot status first turns 'Closed' in 2021 (first `snapshot_date` with `loan_status='Closed'`), and the difference. `closed_loans`, `snapshot_closed`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★★★ &nbsp; (challenge)

Closure tie-out 2022: loans with `closed_date` in 2022 vs loans whose snapshot status first turns 'Closed' in 2022 (first `snapshot_date` with `loan_status='Closed'`), and the difference. `closed_loans`, `snapshot_closed`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q31 &nbsp; ★★★ &nbsp; (challenge)

Closure tie-out 2023: loans with `closed_date` in 2023 vs loans whose snapshot status first turns 'Closed' in 2023 (first `snapshot_date` with `loan_status='Closed'`), and the difference. `closed_loans`, `snapshot_closed`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q32 &nbsp; ★★★ &nbsp; (challenge)

Closure tie-out 2024: loans with `closed_date` in 2024 vs loans whose snapshot status first turns 'Closed' in 2024 (first `snapshot_date` with `loan_status='Closed'`), and the difference. `closed_loans`, `snapshot_closed`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q33 &nbsp; ★★★ &nbsp; (challenge)

Closure tie-out 2025: loans with `closed_date` in 2025 vs loans whose snapshot status first turns 'Closed' in 2025 (first `snapshot_date` with `loan_status='Closed'`), and the difference. `closed_loans`, `snapshot_closed`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q34 &nbsp; ★★ &nbsp; (core)

`'Broker'` channel: loans on `loan` vs settled applications on `loan_application` for that channel, and the difference (internal refinances have no application). `loans`, `settled_apps`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q35 &nbsp; ★★ &nbsp; (core)

`'Branch'` channel: loans on `loan` vs settled applications on `loan_application` for that channel, and the difference (internal refinances have no application). `loans`, `settled_apps`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q36 &nbsp; ★★ &nbsp; (core)

`'Digital'` channel: loans on `loan` vs settled applications on `loan_application` for that channel, and the difference (internal refinances have no application). `loans`, `settled_apps`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q37 &nbsp; ★★ &nbsp; (core)

`'Mobile Lender'` channel: loans on `loan` vs settled applications on `loan_application` for that channel, and the difference (internal refinances have no application). `loans`, `settled_apps`, `diff`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.
