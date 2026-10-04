# DR01 - Timed drill: warm-up (core skills)

`answers/dr01_warmup_timed/qNN.sql` &nbsp;|&nbsp; check with: `grade dr01` or `grade dr01 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Timed drill - interview conditions

Fundamentals under pressure: filters, joins, grouping, NULLs, dates.

**Rules**
* Set a timer: **30 minutes** for 8 questions (about 4 min each).
* No notes, no looking at the solution. Ctrl-click the data dictionary only if you would be allowed a schema in the interview.
* Say your approach out loud (or write 2 lines of plan as a comment) BEFORE writing SQL: *grain? filters? joins? checks?*
* When time is up, stop. Run `grade dr01` and note your score and which questions ran over.
* Questions get harder as you go; skipping and returning is allowed (and realistic).

Scoring guide: 8/8 = ready | 6+ = solid | below 6 = redo the weak concept sets (the question numbers tell you which).

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

How many loans were originated in 2025 and what is their total original amount (0dp)? Return `loans`, `total_amount`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★ &nbsp; (warm-up)

List the 5 product names with the most loans. Return `product_name`, `loans`; sorted by loans descending, then name.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Percentage of applications that were declined (of all applications), 1dp. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q04 &nbsp; ★★ &nbsp; (core)

Customers with no loans at all: how many? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q05 &nbsp; ★★ &nbsp; (core)

Average days between application and decision by channel (1dp), only decided applications. `channel`, `avg_days`; sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

Which 3 states (by property postcode) have the highest total live balance at 2025-12-31? `state`, `balance` (0dp); sorted by balance descending.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

Brokers with more than 100 loans and an average LVR above 70. `broker_id`, `loans`, `avg_lvr` (1dp); sorted by loans descending, then id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **13 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

Number of loans per number of borrowers (1 borrower, 2 borrowers). `borrowers`, `loans`; sorted by borrowers.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.
