# 13 - Pivoting and conditional aggregation

`answers/13_pivot_conditional/qNN.sql` &nbsp;|&nbsp; check with: `grade 13` or `grade 13 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Turn rows into columns (pivot) with conditional aggregation

```
 long (tall)                      wide (pivoted)
 year  purpose   n                year | Refi | Constr | ...
 2023  Refi      900              2023 |  900 |   300
 2023  Constr    300              2024 | ...
```

The portable way:
```
 SELECT year(origination_date) AS yr,
        COUNT(*) FILTER (WHERE purpose = 'Refinance')    AS refi,
        COUNT(*) FILTER (WHERE purpose = 'Construction') AS constr
 FROM loan GROUP BY 1
```
(`SUM(CASE WHEN ... THEN 1 ELSE 0 END)` does the same in every SQL dialect - learn both.)

DuckDB also has `PIVOT loan ON purpose USING COUNT(*) GROUP BY year(...)` and `UNPIVOT` (wide -> long).

Rates and ratios: `AVG(CASE WHEN cond THEN 1.0 ELSE 0 END)` = share meeting `cond`. Use this to build default rates, approval rates, cure rates in one pass.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Loans per year as columns by `rate_type`: `yr`, `fixed`, `variable` counts; sorted by `yr`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Per `channel`: counts of Active, Closed and In Recovery loans as three columns. Return `channel`, `active`, `closed`, `in_recovery`; sorted by `channel`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Use DuckDB `PIVOT` (list the values with `ON col IN (...)`): loans by `channel` (rows) and `loan_status` (columns). Return the pivoted result; columns order will be alphabetical: `channel`, Active, Closed, In Recovery; sorted by `channel`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

Application outcomes by year: `yr`, `settled`, `declined`, `withdrawn`, `lapsed`. Sorted by `yr` (year of application_date).

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

Approval and decline rates by `channel` in one query. Among decided applications: `approved_pct`, `declined_pct` (1dp each). Return `channel`, `approved_pct`, `declined_pct`; sorted by `channel`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

Decline reasons as columns for 'SERV', 'CRED', 'POLICY', 'LVR' by `channel` (counts). Return `channel`, `serv`, `cred`, `policy`, `lvr`; sorted by `channel`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

LVR band x purpose matrix: for loans, count by LVR band (`<=60`, `60-80`, `80-90`, `>90` using CASE) as columns, per `purpose` as rows. Return `purpose`, `le60`, `b60_80`, `b80_90`, `gt90`; sorted by `purpose`. Upper bounds inclusive (a loan at exactly 80 belongs to 60-80).

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

Arrears matrix at 2025-12-31 (non-closed): `repayment_type` rows; columns: `current` (dpd 0), `d1_29`, `d30_89`, `d90plus`, as loan counts. Sorted by `repayment_type`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

UNPIVOT by hand: from a one-row summary of loan counts (`active`, `closed`, `in_recovery`) produce a tall table `status`, `n` using UNION ALL of three selects. Sorted by `status`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★★ &nbsp; (challenge)

Default rate by LVR band. Use `ref_lvr_band` to bucket each loan's `lvr_at_origination_pct` (a band holds LVRs above its `lvr_from_pct` up to and including its `lvr_to_pct`; the first band also includes 0; a NULL upper bound means no cap). For each band return `band_name`, `loans`, `ever_90` (loans that were ever 90+ DPD in any snapshot) and `rate_pct` (2dp). Sorted by `band_id`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Origination mix by year (% of loans): rows = year, columns = share of loans by `channel` (Broker, Branch, Digital, Mobile Lender), 1dp. Return `yr`, `broker_pct`, `branch_pct`, `digital_pct`, `mobile_pct`; sorted by `yr`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Stage migration table (ECL): per `ifrs9_stage` at 2025-12-31 (the last `reporting_date` in `ecl_provision_quarterly`): loans, total EAD (0dp), total ECL (0dp), and coverage % = ECL/EAD (2dp). Return `ifrs9_stage`, `loans`, `ead`, `ecl`, `coverage_pct`; sorted by stage.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

Collections outcome grid: activity types (rows) by whether the outcome was `'Promise to pay'` or `'Payment taken'` (columns). Return `activity_type`, `promises`, `payments`, `total`; sorted by `total` descending then type.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **11 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

Pivot the HPI table: for 2025 year-end (`month_end_date = 2025-12-31`) and 2020 year-end (`2020-12-31`), show each state's index in two columns and the growth %. Return `state`, `idx_2020`, `idx_2025`, `growth_pct` (1dp); sorted by `state`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★★ &nbsp; (challenge)

Complaints per category by year as a pivot using DuckDB `PIVOT` on `year(received_date)` with counts. Return `category` and one column per year ordered ascending; sorted by `category`. Cast the year to text in a subquery first: `SELECT category, CAST(year(received_date) AS VARCHAR) AS yr FROM complaint`.

> Return **9 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★ &nbsp; (core)

`'Purchase - Owner Occupied'` loans by origination year (rows) with one column per channel (Broker, Branch, Digital, Mobile Lender) - conditional counts. `yr`, `broker`, `branch`, `digital`, `mobile`; sorted by year.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q17 &nbsp; ★★ &nbsp; (core)

`'Purchase - Investment'` loans by origination year (rows) with one column per channel (Broker, Branch, Digital, Mobile Lender) - conditional counts. `yr`, `broker`, `branch`, `digital`, `mobile`; sorted by year.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q18 &nbsp; ★★ &nbsp; (core)

`'Refinance'` loans by origination year (rows) with one column per channel (Broker, Branch, Digital, Mobile Lender) - conditional counts. `yr`, `broker`, `branch`, `digital`, `mobile`; sorted by year.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q19 &nbsp; ★★ &nbsp; (core)

`'Equity Release / Top-up'` loans by origination year (rows) with one column per channel (Broker, Branch, Digital, Mobile Lender) - conditional counts. `yr`, `broker`, `branch`, `digital`, `mobile`; sorted by year.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q20 &nbsp; ★★ &nbsp; (core)

`'Construction'` loans by origination year (rows) with one column per channel (Broker, Branch, Digital, Mobile Lender) - conditional counts. `yr`, `broker`, `branch`, `digital`, `mobile`; sorted by year.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q21 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2019: one row per `channel` with columns `settled`, `declined`, `withdrawn`, `lapsed` (counts by `current_status`). Sorted by channel.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q22 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2020: one row per `channel` with columns `settled`, `declined`, `withdrawn`, `lapsed` (counts by `current_status`). Sorted by channel.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q23 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2021: one row per `channel` with columns `settled`, `declined`, `withdrawn`, `lapsed` (counts by `current_status`). Sorted by channel.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q24 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2022: one row per `channel` with columns `settled`, `declined`, `withdrawn`, `lapsed` (counts by `current_status`). Sorted by channel.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q25 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2023: one row per `channel` with columns `settled`, `declined`, `withdrawn`, `lapsed` (counts by `current_status`). Sorted by channel.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q26 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2024: one row per `channel` with columns `settled`, `declined`, `withdrawn`, `lapsed` (counts by `current_status`). Sorted by channel.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q27 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2025: one row per `channel` with columns `settled`, `declined`, `withdrawn`, `lapsed` (counts by `current_status`). Sorted by channel.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q28 &nbsp; ★★ &nbsp; (core)

`'Broker'` loans: per `rate_type` the number of loans in LVR groups `le70`, `70_80`, `80_90`, `gt90` (upper bounds inclusive). `rate_type`, four counts; sorted by rate_type.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q29 &nbsp; ★★ &nbsp; (core)

`'Branch'` loans: per `rate_type` the number of loans in LVR groups `le70`, `70_80`, `80_90`, `gt90` (upper bounds inclusive). `rate_type`, four counts; sorted by rate_type.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q30 &nbsp; ★★ &nbsp; (core)

`'Digital'` loans: per `rate_type` the number of loans in LVR groups `le70`, `70_80`, `80_90`, `gt90` (upper bounds inclusive). `rate_type`, four counts; sorted by rate_type.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q31 &nbsp; ★★ &nbsp; (core)

`'Mobile Lender'` loans: per `rate_type` the number of loans in LVR groups `le70`, `70_80`, `80_90`, `gt90` (upper bounds inclusive). `rate_type`, four counts; sorted by rate_type.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q32 &nbsp; ★★★ &nbsp; (challenge)

Arrears at 2021-12-31 (live loans): one row per `repayment_type` with columns `current`, `d1_29`, `d30_89`, `d90plus` (loan counts) and `rate_30plus` (% 30+, 2 dp). Sorted by repayment_type.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q33 &nbsp; ★★★ &nbsp; (challenge)

Arrears at 2022-12-31 (live loans): one row per `repayment_type` with columns `current`, `d1_29`, `d30_89`, `d90plus` (loan counts) and `rate_30plus` (% 30+, 2 dp). Sorted by repayment_type.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★★★ &nbsp; (challenge)

Arrears at 2023-12-31 (live loans): one row per `repayment_type` with columns `current`, `d1_29`, `d30_89`, `d90plus` (loan counts) and `rate_30plus` (% 30+, 2 dp). Sorted by repayment_type.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★★★ &nbsp; (challenge)

Arrears at 2024-12-31 (live loans): one row per `repayment_type` with columns `current`, `d1_29`, `d30_89`, `d90plus` (loan counts) and `rate_30plus` (% 30+, 2 dp). Sorted by repayment_type.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q36 &nbsp; ★★★ &nbsp; (challenge)

Arrears at 2025-12-31 (live loans): one row per `repayment_type` with columns `current`, `d1_29`, `d30_89`, `d90plus` (loan counts) and `rate_30plus` (% 30+, 2 dp). Sorted by repayment_type.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q37 &nbsp; ★★★ &nbsp; (challenge)

DuckDB `PIVOT`: 2025 loans by `purpose` (rows) and `channel` (columns, listed with `IN`). Return the pivoted table sorted by purpose.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q38 &nbsp; ★★★ &nbsp; (challenge)

DuckDB `UNPIVOT`: from a one-row table of counts `(broker, branch, digital, mobile)` for 2025 loans build a tall `channel`, `loans` table with `UNPIVOT`. Sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.
