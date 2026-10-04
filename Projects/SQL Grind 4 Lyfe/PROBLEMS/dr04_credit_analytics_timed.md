# DR04 - Timed drill: credit-risk analytics case

`answers/dr04_credit_analytics_timed/qNN.sql` &nbsp;|&nbsp; check with: `grade dr04` or `grade dr04 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Timed drill - interview conditions

Case-study style, as in a bank's analytics interview: definitions matter. Write down your definition of the live book first.

**Rules**
* Set a timer: **45 minutes** for 9 questions (about 5 min each).
* No notes, no looking at the solution. Ctrl-click the data dictionary only if you would be allowed a schema in the interview.
* Say your approach out loud (or write 2 lines of plan as a comment) BEFORE writing SQL: *grain? filters? joins? checks?*
* When time is up, stop. Run `grade dr04` and note your score and which questions ran over.
* Questions get harder as you go; skipping and returning is allowed (and realistic).

Scoring guide: 9/9 = ready | 7+ = solid | below 7 = redo the weak concept sets (the question numbers tell you which).

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Live book at 2025-12-31: loans and balance (0dp). `loans`, `balance`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★★ &nbsp; (core)

90+ DPD rate by balance (2dp %) at each year-end 2021-2025. `snapshot_date`, `rate_pct`; sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★★ &nbsp; (core)

Investor vs owner-occupier 30+ DPD rate (count, 2dp) at 2025-12-31. `occupancy`, `rate_pct`; sorted by occupancy.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

Which origination year has the worst ever-90+ rate? Return the year and rate (2dp) - top 1. `yr`, `ever90_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★★ &nbsp; (challenge)

Roll rate: of live loans at 30-59 DPD at 2025-11-30, what % were 60+ DPD at 2025-12-31 (non-closed, 1dp)? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q06 &nbsp; ★★★ &nbsp; (challenge)

Stage 2 + 3 share of live EAD at 2025-12-31 (2dp %). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q07 &nbsp; ★★★ &nbsp; (challenge)

Estimate the payment-shock exposure of fixed loans expiring in the next 6 months (after 2025-12-31, up to 2026-06-30): count and balance (0dp). `loans`, `balance`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Which broker has the highest 90-plus DPD balance rate among brokers with live balance above $100m? `broker_id`, `rate_pct` (2dp) - one row.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★★ &nbsp; (challenge)

New lending by quarter of 2025 alongside the number of loans closed in each quarter. Return `quarter` (1-4), `new_amount` (0dp), `closed_loans`; sorted by quarter.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.
