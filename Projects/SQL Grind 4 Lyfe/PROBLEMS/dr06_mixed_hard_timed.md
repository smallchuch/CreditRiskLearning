# DR06 - Timed drill: mixed hard set

`answers/dr06_mixed_hard_timed/qNN.sql` &nbsp;|&nbsp; check with: `grade dr06` or `grade dr06 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Timed drill - interview conditions

The hardest mix: close to a senior analyst final round. Expect to combine windows, CTEs and careful definitions.

**Rules**
* Set a timer: **60 minutes** for 8 questions (about 8 min each).
* No notes, no looking at the solution. Ctrl-click the data dictionary only if you would be allowed a schema in the interview.
* Say your approach out loud (or write 2 lines of plan as a comment) BEFORE writing SQL: *grain? filters? joins? checks?*
* When time is up, stop. Run `grade dr06` and note your score and which questions ran over.
* Questions get harder as you go; skipping and returning is allowed (and realistic).

Scoring guide: 8/8 = ready | 6+ = solid | below 6 = redo the weak concept sets (the question numbers tell you which).

---

## Problems

### Q01 &nbsp; ★★ &nbsp; (core)

The month with the most originations in each year (ties earliest month). `yr`, `month_no`, `loans`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★★★ &nbsp; (challenge)

Customers who have 2+ loans and whose second loan was larger than the first. Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q03 &nbsp; ★★★ &nbsp; (challenge)

Longest streak of consecutive months with 30+ DPD for any loan - and how many loans achieved that max streak. `max_streak`, `loans`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q04 &nbsp; ★★★ &nbsp; (challenge)

For loans originated in 2022, what % were still open 36 months after origination (has a non-closed snapshot at MOB 36)? 1dp. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q05 &nbsp; ★★★ &nbsp; (challenge)

Customers who were ever 90+ DPD on a loan and still hold another live loan (not 90+) at 2025-12-31. Count distinct customers. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q06 &nbsp; ★★★ &nbsp; (challenge)

Contribution to ECL: the top 10 loans by ECL at 2025-12-31 and the % of total ECL they represent (2dp, as `top10_share_pct`) and their combined ECL (0dp). One row: `top10_ecl`, `top10_share_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q07 &nbsp; ★★★ &nbsp; (challenge)

Cohort retention matrix: for loans originated in H1 2022 (Jan-Jun), the % still open at MOB 6, 12, 18, 24. `mob`, `open_pct` (1dp); sorted by mob.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★★ &nbsp; (challenge)

First-time defaulters by origination channel and year (2021-2024): number of loans whose first ever 90+ DPD happened within 24 months of origination, divided by loans originated - the 24-month default rate (2dp). `yr`, `broker_pct`, `branch_pct`, `digital_pct`, `mobile_pct`; sorted by year.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.
