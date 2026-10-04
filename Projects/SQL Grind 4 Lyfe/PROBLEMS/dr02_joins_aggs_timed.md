# DR02 - Timed drill: joins and aggregates

`answers/dr02_joins_aggs_timed/qNN.sql` &nbsp;|&nbsp; check with: `grade dr02` or `grade dr02 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Timed drill - interview conditions

The bread-and-butter interview round: join three tables, aggregate, filter groups.

**Rules**
* Set a timer: **40 minutes** for 10 questions (about 4 min each).
* No notes, no looking at the solution. Ctrl-click the data dictionary only if you would be allowed a schema in the interview.
* Say your approach out loud (or write 2 lines of plan as a comment) BEFORE writing SQL: *grain? filters? joins? checks?*
* When time is up, stop. Run `grade dr02` and note your score and which questions ran over.
* Questions get harder as you go; skipping and returning is allowed (and realistic).

Scoring guide: 10/10 = ready | 8+ = solid | below 8 = redo the weak concept sets (the question numbers tell you which).

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Top 5 branches by total original lending in 2025 (branch name, $0dp). `branch_name`, `amount`; sorted by amount descending.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Approval rate (decided only, 1dp) by broker tier (A/B/C) using `dim_broker`. `broker_tier`, `approval_pct`; sorted by tier.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★★ &nbsp; (core)

Average bureau score (0dp) of declined vs approved applicants (primary applicant). `decision`, `avg_score`; sorted by decision. Decided applications only.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

Assessors who approved more than 1,000 applications: `assessor_staff_id`, `full_name`, `approved`; sorted by approved descending, id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **39 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

Customers with both an investment loan and an owner-occupied purchase loan (as primary): count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q06 &nbsp; ★★ &nbsp; (core)

Total live balance (0dp) by customer `segment` at 2025-12-31 (primary customer). `segment`, `balance`; sorted by segment.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★★ &nbsp; (challenge)

Share of loans per `channel` that have a co-borrower (1dp). `channel`, `joint_pct`; sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Branches whose average loan size in 2025 is above the bank-wide average loan size in 2025. `branch_name`, `avg_amount` (0dp); sorted by avg descending, name.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **21 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★★ &nbsp; (challenge)

For each year, the broker with the most loans (ties alphabetical by firm name). `yr`, `firm_name`, `loans`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★★ &nbsp; (challenge)

Customers who applied more than once in the same year and were declined at least once that year. Count distinct customers. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.
