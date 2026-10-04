# DR05 - Timed drill: dirty data

`answers/dr05_data_quality_timed/qNN.sql` &nbsp;|&nbsp; check with: `grade dr05` or `grade dr05 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Timed drill - interview conditions

You've been handed an unfamiliar extract. Find the problems fast. Each question is a typical data-validation ask.

**Rules**
* Set a timer: **40 minutes** for 9 questions (about 4 min each).
* No notes, no looking at the solution. Ctrl-click the data dictionary only if you would be allowed a schema in the interview.
* Say your approach out loud (or write 2 lines of plan as a comment) BEFORE writing SQL: *grain? filters? joins? checks?*
* When time is up, stop. Run `grade dr05` and note your score and which questions ran over.
* Questions get harder as you go; skipping and returning is allowed (and realistic).

Scoring guide: 9/9 = ready | 7+ = solid | below 7 = redo the weak concept sets (the question numbers tell you which).

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Duplicate applications: pairs of applications by the same `primary_customer_id` on the same `application_date` for the same `requested_amount`. Count the groups. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★★ &nbsp; (core)

Customers with an impossible age at 2025-12-31 (under 18 or over 100) among those with a DOB. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q03 &nbsp; ★★ &nbsp; (core)

Loans where `maturity_date` is before `origination_date` or `term_months` <= 0. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q04 &nbsp; ★★ &nbsp; (core)

Rows in `loan_monthly_snapshot` with a negative balance or `days_past_due` < 0. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q05 &nbsp; ★★ &nbsp; (core)

Interest rates outside 1%-15% in the snapshot (non-closed). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q06 &nbsp; ★★★ &nbsp; (challenge)

Status events out of order: applications where a 'Settled' event timestamp is before the application's 'Submitted' timestamp (use MIN per status). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q07 &nbsp; ★★★ &nbsp; (challenge)

Applications whose `current_status` disagrees with the LAST event in `application_status_history` (latest by ts then event_id). Count. One number. (Some disagreement is expected from duplicate loads - do you understand why?)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Customers whose `postcode` is not in `dim_postcode`. Count and the % of customers (2dp). `customers`, `pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q09 &nbsp; ★★★ &nbsp; (challenge)

Same person, different customer ids: pairs sharing the same cleaned email (lowercase, trimmed) - the number of customer rows that share an email with at least one other customer. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.
