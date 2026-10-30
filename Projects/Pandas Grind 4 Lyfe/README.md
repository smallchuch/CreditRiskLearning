# Pandas Grind 4 Lyfe

135 pandas / NumPy / Python problems against the same synthetic mortgage bank as SQL Grind 4 Lyfe
(`..\..\Datasets\Synthetic Bank\parquet\`). Write each answer in its own `.py` file; a checker tells you PASS / FAIL in a
few seconds; Claude reviews the ones you want a second opinion on.

The sets follow McKinney's *Python for Data Analysis* (3rd ed.), so you can read a chapter and then drill it, and they
target the things that trip you up in the real notebooks: types and methods, index alignment, actuals vs predictions,
groupby, merges, reshaping, ties in deciles.

## Your 15-minute routine

```
 1.  grade --next            show the next question you haven't passed   (grade --random for any one)
 2.  open answers\<concept>\qNN.py in VS Code. The setup cell is done for you; write under "# %% your answer"
 3.  "Run Cell" (or Shift+Enter) to try things in the Interactive window, until `result` looks right
 4.  grade <concept> qNN     PASS / FAIL (with a hint of why)
 5.  stuck for 10 min?       grade <concept> qNN --expected   (first rows of the right answer)
     really stuck?           grade <concept> qNN --solution   (the reference code; logged as "peeked")
 6.  end of the week: grade --review, then ask Claude "review my pandas grind"
```

**Setup (once):** run from the venv you use for CreditRiskLearning (it needs pandas, numpy and pyarrow; the model sets
also use scikit-learn and scipy). In the folder, `grade` runs `grade.bat`, which runs `grade.py`.
In PowerShell type `.\grade` (PowerShell won't run a file from the current folder without the `.\`).

## Commands

| Command | Does |
|---|---|
| `grade --next` / `grade --next 06` | next unpassed question (overall / in concept 06) |
| `grade --random` / `grade --random cr` | random unpassed question |
| `grade 06` | grade every answer you've written in concept 06 |
| `grade 06 q03` | grade one question |
| `grade` | grade everything you've written |
| `grade --status` | progress table |
| `grade 06 q03 --expected` | peek at the first rows of the expected result |
| `grade 06 q03 --solution` | show the reference solution |
| `grade --review` | rebuild `progress\REVIEW_ME.md` for Claude |

## The problem sets (`PROBLEMS\*.md` has the primer, diagrams and all questions)

**Core (01-12).** Read the primer first. Each set runs warm-up (one star) to challenge (three stars).

| # | Concept | McKinney | # | Concept | McKinney |
|---|---|---|---|---|---|
| 01 | Python basics: types, f-strings, dicts, loops | 2, 3 | 07 | Merge, join, concat | 8 |
| 02 | NumPy: arrays, masks, vectorised maths | 4 | 08 | Reshape: pivot, unstack, melt, crosstab | 8, 10 |
| 03 | Selecting, filtering, sorting | 5 | 09 | Binning and ranking: cut, qcut, rank | 5, 7 |
| 04 | Index, labels and alignment | 5 | 10 | Dates and time series | 11 |
| 05 | Missing values, strings, duplicates | 7 | 11 | shift, diff, cumulative, rolling | 10, 11 |
| 06 | GroupBy: aggregate, transform, filter | 10 | 12 | Loops over dicts, functions, building tables | 3, 10 |

**Credit-risk scenarios (cr01-cr05).** Portfolio and concentration, arrears and roll rates, vintage curves, score
evaluation (deciles, Gini, KS, capture), origination and serviceability.

## How checking works

* Each answer file is **run fresh, on its own**. Anything it needs (filters, helper columns) must be in the file.
  No leftovers from another cell or another question can help or hurt you, which is exactly the "Restart and Run All" test.
* Put your final answer in `result`. It can be a DataFrame, Series, list, dict or a single value.
* A **meaningful index** (group keys, labels) counts as the leading columns, so a `groupby(...).mean()` Series is fine
  as it is. A plain integer index (0, 1, 2 ... or what's left after filtering) is ignored.
* Column **order** matters, names don't. Row order matters only when the question says "sorted".
* Numbers match within a small tolerance (usually 0.011, tighter where the question asks for 3 or 4 dp).
  `NaN`, `None` and `NaT` all count as missing. Dates compare as `YYYY-MM-DD`.
* Your attempts are logged to `progress\attempts.csv` (PASS / FAIL / ERROR / PEEKED, timing).

## The data, as you'll use it

```python
from grind import load
loan = load('loan')          # every call returns a fresh copy
```
Money, rate and ratio columns arrive as `float64`; dates arrive as `datetime64` (so `.dt` works). The stubs load the
tables each question needs, with these short names:

| Table | Variable | Table | Variable |
|---|---|---|---|
| `loan_monthly_snapshot` | `snap` | `application_assessment` | `assess` |
| `loan_application` | `app` | `application_applicant` | `applicant` |
| `credit_bureau_report` | `bureau` | everything else | its own name |

**The live book** (used all over): `snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')]`.
The data ends at 2025-12-31. `..\..\Datasets\Synthetic Bank\DATA_DICTIONARY.md` describes every column.

## Review (the "Claude checks my work" part)

The checker only knows right or wrong. Claude can say *how* you could write it better: readability, a vectorised
version of a loop, a result that passed by luck, what to practise next.
Run `grade --review`, then tell Claude: **"review my pandas grind"**. Claude reads `progress\REVIEW_ME.md` (your code with
its latest status).

## Tips for when your brain is tired
* One question is a complete session. `grade --next`, do it, stop.
* FAIL is information. Read the "column count" and "row count" lines first: they usually mean the index is in the wrong
  place (`.reset_index()`) or a filter is missing (the live book!).
* `print(type(x))`, `x.shape`, `x.head()` and `x.index` answer most "why doesn't this work" questions.
* Keep a `notes.md` of patterns that tripped you up. The primers are short on purpose; re-read them.

## Folder map
```
 PROBLEMS\        the questions + primers (read these)   answers\<concept>\qNN.py   (you write these)
 progress\        attempts.csv, REVIEW_ME.md             _grader\   expected results (don't open - spoilers)
 _source\         problem-set source + build script      config.json   path to the Parquet folder
 grind.py         load() helper                          grade.py / grade.bat   the checker
```
If the data is ever rebuilt, run `python _source\build_problem_sets.py` to refresh the expected results
(it never overwrites your answers). Add `--selftest` to check every reference solution through the grader.
