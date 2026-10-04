# DR03 - Timed drill: window functions

`answers/dr03_windows_timed/qNN.sql` &nbsp;|&nbsp; check with: `grade dr03` or `grade dr03 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Timed drill - interview conditions

Rankings, running totals, LAG/LEAD and top-N - the favourite of interviewers.

**Rules**
* Set a timer: **40 minutes** for 8 questions (about 5 min each).
* No notes, no looking at the solution. Ctrl-click the data dictionary only if you would be allowed a schema in the interview.
* Say your approach out loud (or write 2 lines of plan as a comment) BEFORE writing SQL: *grain? filters? joins? checks?*
* When time is up, stop. Run `grade dr03` and note your score and which questions ran over.
* Questions get harder as you go; skipping and returning is allowed (and realistic).

Scoring guide: 8/8 = ready | 6+ = solid | below 6 = redo the weak concept sets (the question numbers tell you which).

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Rank the 5 largest live balances at 2025-12-31 with ROW_NUMBER (tie `loan_id`). `loan_id`, `closing_balance`, `rn`; sorted by rn.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★★ &nbsp; (core)

For each state of property, the loan with the highest live balance at 2025-12-31 (tie `loan_id`). `state`, `loan_id`, `closing_balance`; sorted by state.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★★ &nbsp; (core)

Monthly application counts for 2025 with the change vs the previous month. `month_start`, `apps`, `change`; sorted by month (change NULL for Jan).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

Running total of new lending ($, 0dp) by month for 2025. `month_start`, `running_total`; sorted by month.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★★ &nbsp; (challenge)

Each customer's second loan: `primary_customer_id`, `loan_id`, `origination_date` for customers with at least 2 loans (order by date then loan_id). Return the first 10 by customer id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★★ &nbsp; (challenge)

Days between a customer's first and second loan: median across customers with 2+ loans (1dp). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q07 &nbsp; ★★★ &nbsp; (challenge)

3-month moving average of 90+ DPD loan counts at month-ends of 2025 (use all history for the window). `snapshot_date`, `n90`, `ma3` (1dp); 2025 months only; sorted by date. Live loans.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Percentile of each product's average original loan size across products: `product_id`, `avg_amount` (0dp), `pct_rank` (2dp, ordered ascending); sorted by product_id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.
