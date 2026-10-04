# SQL Grind 4 Lyfe

1,360+ SQL problems against a realistic synthetic mortgage-bank database (`..\..\Datasets\Synthetic Bank\bank.duckdb`).
Write each answer in its own `.sql` file; a checker tells you PASS / FAIL in a second; Claude reviews the ones you want a second opinion on.

## Your 30-minute routine

```
 1.  grade --next            show the next question you haven't passed
 2.  open answers\<concept>\qNN.sql in VS Code, write your SELECT under the comment header
 3.  run it in the DuckDB CLI / VS Code however you like, until the output looks right
 4.  grade <concept> qNN     PASS / FAIL (with a hint of why)
 5.  stuck for 10 min?       grade <concept> qNN --expected   (shows the first rows of the right answer)
     really stuck?           grade <concept> qNN --solution   (shows the reference SQL; logged as "peeked")
 6.  at the end of the week: ask Claude "review my SQL grind" - see Review below
```

One-time setup (Anaconda prompt or any terminal): `pip install duckdb` - that is the only requirement.
In the folder, `grade` runs `grade.bat` which runs `grade.py`.

## Commands

| Command | Does |
|---|---|
| `grade --next` / `grade --next 05` | next unpassed question (overall / in concept 05) |
| `grade --random` / `grade --random cr` | random unpassed question (good when you can't decide) |
| `grade 05` | grade every answer you've written in concept 05 |
| `grade 05 q03` | grade one question |
| `grade` | grade everything you've written |
| `grade --status` | progress table |
| `grade 05 q03 --expected` | peek at the first rows of the expected result |
| `grade 05 q03 --solution` | show the reference solution |
| `grade --review` | rebuild `progress\REVIEW_ME.md` for Claude |

## The problem sets (`PROBLEMS\*.md` has the primer, diagrams and all questions)

**Core SQL (01-17)** - read the primer first, then work in order. Each set runs warm-up (one star) to challenge (three stars).

| # | Concept | # | Concept |
|---|---|---|---|
| 01 | SELECT / WHERE / ORDER BY / LIMIT | 10 | Window I: ranking, top-N |
| 02 | Expressions, CASE, functions | 11 | Window II: LAG/LEAD, running totals |
| 03 | NULLs | 12 | UNION / INTERSECT / EXCEPT |
| 04 | Dates | 13 | Pivot and conditional aggregation |
| 05 | Aggregation, GROUP BY, HAVING | 14 | Data quality, gaps and islands |
| 06 | Joins (basic) | 15 | Time series, cohorts, point-in-time |
| 07 | Joins (anti, semi, self, range, fan-out) | 16 | DDL / DML / views (scratch sandbox) |
| 08 | Subqueries | 17 | Rewriting for speed and clarity |
| 09 | CTEs and recursion | | |

**Credit-risk scenarios (cr01-cr11)** - things you'd really be asked at a bank: portfolio and concentration, arrears, roll rates, vintage curves, origination and serviceability, pricing and rate shock, collateral, hardship and collections, loss and ECL, reconciliations, the monthly reporting pack.

**Timed drills (dr01-dr06)** - interview conditions. Set a timer (the primer says how long), no peeking, grade at the end, note your score.

## How checking works

* Compares your **result set** with the reference result. Column **order** matters (names don't). Row order matters only when the question says "sorted". Numbers match within 0.011.
* Your file can have several statements; the **last one returning rows** is graded.
* Tables you create must live in the **`scratch`** schema (e.g. `CREATE TABLE scratch.t AS ...`) - it's an in-memory sandbox, wiped each run. The bank database is opened **read-only**, so you can't break it.
* Your attempts are logged to `progress\attempts.csv` (PASS/FAIL/ERROR/PEEKED, timing).

## Review (the "Claude checks my work" part)

The checker only knows right or wrong. Claude can say *how* you could write it better (readability, performance, edge cases, interview style).
Run `grade --review`, then tell Claude: **"review my SQL grind"**. Claude reads `progress\REVIEW_ME.md` (your queries with their results and PASS/FAIL), and comments on style, correctness-by-luck, and what to practise next.

## Tips for when your brain is tired
* One question is a complete session. `grade --next`, do it, stop.
* FAIL is information: re-read the "sorted by..." and "N column(s)" lines first, then check NULLs and the live-book definition (`snapshot_date = '2025-12-31'` and `loan_status <> 'Closed'`).
* Keep a `notes.md` of patterns that tripped you up. The primers are short on purpose - re-read them.

## Folder map
```
 PROBLEMS\        the questions (read these)         answers\<concept>\qNN.sql   (you write these)
 progress\        attempts.csv, REVIEW_ME.md          _grader\   expected results (don't open - spoilers)
 _source\         problem-set source + build script   config.json   path to bank.duckdb
```
If the database is ever rebuilt, run `python _source\build_problem_sets.py` to refresh the expected results (it never overwrites your answers).
