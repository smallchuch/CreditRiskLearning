# cr03 - Vintage analysis

`answers/cr03_vintage/qNN.py` &nbsp;|&nbsp; check with: `grade cr03` or `grade cr03 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

**Credit-risk scenario.** Vintage analysis: the warm-up for Freddie Mac stage 02. Patterns from sets 08, 10, 11.

## A vintage curve is a pivot

```
 one row per loan-month (snap)            ->   vintage x MOB table
 loan  vintage  mob  dpd  ever90_so_far          MOB:   6     12     18     24
 A     2021     0    0    0                      2019  0.4%  1.1%  1.8%  2.2%
 A     2021     1    0    0                      2020  0.3%  0.9%  1.6%  2.1%
 ...                                             2021  ...
```

## The recipe (cumulative ever-90 by MOB)
1. Vintage of each loan = origination year (or quarter: `dt.to_period('Q')`).
2. For each loan, the **first MOB** at which it reached 90+ (NaN if never).
3. For each vintage and target MOB m: share of the vintage's loans whose first-90+ MOB is `<= m`.
4. **Denominator = every loan in the vintage**, including ones that closed early (they can't go bad later; that's the
   usual "cumulative bad rate" convention).

## Censoring
A 2025 vintage can't have a MOB-24 value yet. Only include vintages old enough for the MOB you're reporting
(the questions say which).

## Point-in-time vs cumulative
- **Cumulative** ever-90 by MOB 12: went bad at any point up to MOB 12. Only goes up with MOB.
- **Point-in-time** 30+ at MOB 12: in arrears *at* MOB 12, among loans still on book then. Can go down (cures).

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Loans per **origination quarter** for 2023 vintages, as strings like `'2023Q1'`. Return `vintage`, `loans`; sorted by `vintage`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q02 &nbsp; ★★ &nbsp; (core)

Cumulative ever-90 rate **by MOB 12** for vintages 2019 to 2024: the percentage of each vintage's loans whose first
90+ month-end came at `months_on_book <= 12`. Denominator = all loans in the vintage. Return `vintage`, `pct` (2 dp);
sorted by `vintage`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `loan`

### Q03 &nbsp; ★★★ &nbsp; (challenge)

The full vintage table: rows = vintages 2019 to 2023, columns = MOB 6, 12, 18, 24, values = cumulative ever-90 % by
that MOB (2 dp). Return `vintage`, `6`, `12`, `18`, `24`; sorted by `vintage`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `loan`

<details><summary>hint</summary>

One column per MOB is a natural loop: `for m in [6, 12, 18, 24]`.

</details>

### Q04 &nbsp; ★★ &nbsp; (core)

**Point-in-time** 30+ rate at MOB 12 by vintage 2019 to 2024: among loans that have a snapshot at `months_on_book == 12`
(and are not `'Closed'` in it), the percentage with `days_past_due >= 30` in that snapshot. Return `vintage`, `pct` (2 dp);
sorted by `vintage`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `loan`

### Q05 &nbsp; ★★★ &nbsp; (challenge)

**Balance-weighted** cumulative ever-90 by MOB 24 for vintages 2019 to 2023: original amount of loans that went 90+ by
MOB 24 / original amount of the whole vintage, as % (2 dp). Return `vintage`, `pct_by_amount`; sorted by `vintage`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `loan`

### Q06 &nbsp; ★★★ &nbsp; (challenge)

Survival: for vintages 2019 to 2023, the percentage of each vintage's loans that still had a non-`'Closed'` snapshot at
MOB 24. Return `vintage`, `pct_open_mob24` (2 dp); sorted by `vintage`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `loan`
