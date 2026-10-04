# 12 - UNION, INTERSECT, EXCEPT

`answers/12_set_operations/qNN.sql` &nbsp;|&nbsp; check with: `grade 12` or `grade 12 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Set operations stack results vertically (joins glue sideways)

```
 Query A (3 rows)         Query B (3 rows)
 +----+                   +----+
 | 1  |                   | 2  |
 | 2  |                   | 3  |
 | 3  |                   | 4  |
 +----+                   +----+

 UNION ALL  -> 1,2,3,2,3,4   (keep everything)
 UNION      -> 1,2,3,4       (remove duplicates)
 INTERSECT  -> 2,3           (in both)
 EXCEPT     -> 1             (in A but not B)
```

Rules: same number of columns, compatible types, column names come from the **first** query.
`UNION ALL` is faster and what you want when you know there are no dupes (or want them).
`EXCEPT` is a clean way to reconcile: "what is in source A that is missing from B?"

Common credit-risk uses: stacking monthly extracts, reconciling two systems, finding customers in one product but not another.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Stack two lists: `product_id`s 1-3 UNION ALL product_ids 3-5 from `dim_product`. Return `product_id` sorted ascending (3 appears twice).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Same lists with `UNION` (dedupe). Return `product_id` sorted.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Customers who are primary on BOTH a 'Purchase - Owner Occupied' loan AND a 'Purchase - Investment' loan (INTERSECT). Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q04 &nbsp; ★★ &nbsp; (core)

Customers who applied (primary) but never got a loan (EXCEPT). Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q05 &nbsp; ★★ &nbsp; (core)

A combined events feed: UNION ALL of `loan_event` (loan_id, event_date, event_type) and hardship starts (loan_id, start_date, 'Hardship start') for loans 1-300. Return `loan_id`, `event_date`, `event_type`, sorted by `loan_id`, `event_date`, `event_type`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **639 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

Customers that appear in the `complaint` table but have NO loan as primary or co-borrower. Use EXCEPT on `customer_id` vs `loan_borrower.customer_id`. Count them. (May be 0.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q07 &nbsp; ★★ &nbsp; (core)

One list of every person-ish key: UNION of `primary_customer_id` from `loan_application` and `customer_id` from `application_applicant`. How many distinct customer ids? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q08 &nbsp; ★★ &nbsp; (core)

Applications with a bureau report but no assessment row (EXCEPT on application_id). Count. One number (expect 0).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q09 &nbsp; ★★ &nbsp; (core)

Reconcile loans to snapshots: loans with no rows in `loan_monthly_snapshot` (EXCEPT). Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q10 &nbsp; ★★ &nbsp; (core)

Reconcile loan status: loans marked `'Closed'` on `loan` but whose latest snapshot status is NOT 'Closed' (EXCEPT of loan_ids). Count. One number (expect 0).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Add a total row: per `channel` loan counts, UNION ALL a 'ALL' row with the grand total. Return `channel`, `loans`; sorted with channels alphabetically and 'ALL' last (hint: sort by `channel = 'ALL'`, then channel).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Loans in recovery or with a loss record: UNION of loan_ids from `loan_loss` and loans with `loan_status='In Recovery'`. Count the union. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

Symmetric difference: customers in `customer` whose cleaned (lowercase) email appears more than once vs customers with a mobile starting '+61'. How many customers appear in exactly ONE of the two groups? Use UNION of two EXCEPTs. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

Month-by-month stack: UNION ALL 2023, 2024 and 2025 loan counts per month number into one table of `yr`, `mon`, `loans`. Return the rows for months 1-3 only, sorted by `yr`, `mon`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **9 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★★ &nbsp; (challenge)

Funnel as a stack: one result with `stage` and `apps` using UNION ALL: 'Lodged' = all applications; 'Decided' = decision not null; 'Approved' = decision Approved; 'Settled' = current_status Settled. Sorted by `apps` descending.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★★ &nbsp; (challenge)

INTERSECT with multiple columns: (`purpose`, `channel`) combinations that appear both in `loan` and in `loan_application`. Return the pairs sorted by purpose, channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **20 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q17 &nbsp; ★★ &nbsp; (core)

INTERSECT: customers who lodged an application in 2019 AND in 2020 (primary). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★ &nbsp; (core)

INTERSECT: customers who lodged an application in 2020 AND in 2021 (primary). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★★ &nbsp; (core)

INTERSECT: customers who lodged an application in 2021 AND in 2022 (primary). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★★ &nbsp; (core)

INTERSECT: customers who lodged an application in 2022 AND in 2023 (primary). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★ &nbsp; (core)

INTERSECT: customers who lodged an application in 2023 AND in 2024 (primary). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★ &nbsp; (core)

INTERSECT: customers who lodged an application in 2024 AND in 2025 (primary). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★ &nbsp; (core)

EXCEPT: customers who applied in 2019 but did NOT apply in 2020. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★★ &nbsp; (core)

EXCEPT: customers who applied in 2020 but did NOT apply in 2021. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★★ &nbsp; (core)

EXCEPT: customers who applied in 2021 but did NOT apply in 2022. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★★ &nbsp; (core)

EXCEPT: customers who applied in 2022 but did NOT apply in 2023. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★★ &nbsp; (core)

EXCEPT: customers who applied in 2023 but did NOT apply in 2024. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★★ &nbsp; (core)

EXCEPT: customers who applied in 2024 but did NOT apply in 2025. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★★ &nbsp; (core)

Customers (primary) with BOTH a `'Purchase - Owner Occupied'` and a `'Purchase - Investment'` loan: count via `INTERSECT`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★★ &nbsp; (core)

Customers (primary) with BOTH a `'Purchase - Owner Occupied'` and a `'Refinance'` loan: count via `INTERSECT`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q31 &nbsp; ★★ &nbsp; (core)

Customers (primary) with BOTH a `'Purchase - Owner Occupied'` and a `'Equity Release / Top-up'` loan: count via `INTERSECT`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q32 &nbsp; ★★ &nbsp; (core)

Customers (primary) with BOTH a `'Purchase - Owner Occupied'` and a `'Construction'` loan: count via `INTERSECT`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q33 &nbsp; ★★ &nbsp; (core)

Customers (primary) with BOTH a `'Purchase - Investment'` and a `'Refinance'` loan: count via `INTERSECT`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q34 &nbsp; ★★ &nbsp; (core)

Customers (primary) with BOTH a `'Purchase - Investment'` and a `'Equity Release / Top-up'` loan: count via `INTERSECT`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q35 &nbsp; ★★★ &nbsp; (challenge)

Customers with a loan via `'Broker'` but none via any other channel (`EXCEPT`). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q36 &nbsp; ★★★ &nbsp; (challenge)

Customers with a loan via `'Branch'` but none via any other channel (`EXCEPT`). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q37 &nbsp; ★★★ &nbsp; (challenge)

Customers with a loan via `'Digital'` but none via any other channel (`EXCEPT`). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q38 &nbsp; ★★★ &nbsp; (challenge)

Customers with a loan via `'Mobile Lender'` but none via any other channel (`EXCEPT`). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q39 &nbsp; ★★ &nbsp; (core)

`UNION ALL` of two periods: loan counts per `channel` for 2020 and 2021 in one table with a `yr` column. `yr`, `channel`, `loans`; sorted by yr, channel.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q40 &nbsp; ★★ &nbsp; (core)

`UNION ALL` of two periods: loan counts per `channel` for 2022 and 2023 in one table with a `yr` column. `yr`, `channel`, `loans`; sorted by yr, channel.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q41 &nbsp; ★★ &nbsp; (core)

`UNION ALL` of two periods: loan counts per `channel` for 2024 and 2025 in one table with a `yr` column. `yr`, `channel`, `loans`; sorted by yr, channel.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q42 &nbsp; ★★★ &nbsp; (challenge)

Loans closed by refinance elsewhere that never had a retention discount event (EXCEPT of loan_ids). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q43 &nbsp; ★★★ &nbsp; (challenge)

Customers who were declined at least once but later have a loan: `INTERSECT` declined customers with loan customers. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.
