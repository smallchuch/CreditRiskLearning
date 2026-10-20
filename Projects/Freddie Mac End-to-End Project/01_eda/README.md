# freddie-pd-build

> **Analysis** · created 2026-10-16 · status: 🟡 in progress

## Brief
| | |
|---|---|
| **Question** | *One sentence. What decision does this inform?* |
| **Stakeholders** | *Who asked, who decides, who reviews* |
| **Deadline** | |
| **Scope** | *In / out* |
| **Definitions** | *Every term a reader could interpret two ways: bad, active, arrears, cohort …* |
| **Data** | *Source systems, snapshot date (also in `config.yml`)* |

## Answer
*Fill in last: the headline in 2–3 sentences, with the numbers.*

## Workflow
| File | Stage |
|---|---|
| `sql/01_extract.sql` | the extract |
| `notebooks/01_data.ipynb` | Data & quality: Extract the data the question needs and make sure it can be trusted. |
| `notebooks/02_eda.ipynb` | Exploration: Understand the data before answering the question: distributions, trends, the obvious drivers. |
| `notebooks/03_analysis.ipynb` | Analysis: Answer the question. One section per sub-question in the README brief. |
| `notebooks/04_findings.ipynb` | Findings & outputs: Turn results into the tables and figures the deck/report reads. No new analysis here. |
| `deliverables/` | Quarto deck + report (`quarto render deliverables/`) |


Each notebook reads the previous stage's dataset from `data/interim/` and writes its own. Finished tables go
to `outputs/tables/` via `proj.write_table()`, which logs lineage to `outputs/manifest.json`.

## Decisions log
| Date | Decision | Why | Who |
|---|---|---|---|
| 2026-10-16 | Project created | | |

## Open questions
-
