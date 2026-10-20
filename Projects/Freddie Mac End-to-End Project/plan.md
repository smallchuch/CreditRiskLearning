# Freddie Mac Mortgages: Vintage Analysis + Portfolio Dashboard

**Scope (Oct 2026):** vintage analysis only, then a portfolio dashboard built on its outputs.
PD, EAD, LGD and the IFRS 9 ECL layer are parked (see "Parked" at the bottom).

**The question this project answers:**
*How do default and prepayment build up over a mortgage's life, and how much does that depend on when it was written and who it was written to?*

---

## 1. Data

- Freddie Mac Single-Family Loan-Level **Sample Dataset** (50,000 loans per origination year, via Clarity).
- Years: **2006, 2007, 2010, 2016**. Build everything on **2007** first, then loop the other years through the same code.
- Each `sample_YYYY.zip`:
  - `sample_orig_YYYY.txt`: one row per loan (traits at origination)
  - `sample_perf_YYYY.txt`: one row per loan per month (performance history)
  - Pipe delimited, no header; join on **Loan Sequence Number**.
- **Raw files:** `data/raw/sample_YYYY.zip` (all 4 years). Read straight from the zip with `zipfile`, no need to unzip.
- Sizes (uncompressed): orig ~6 MB per year, perf ~350-390 MB per year (2007: 50,000 loans, 3,012,061 loan-months). Use `usecols` + dtypes when reading perf.
- Avoid 2019-2021 (COVID forbearance distorts delinquency) and 2022+ (too young).

| Year | Story it tells |
|---|---|
| 2006 | Pre-GFC loose lending |
| 2007 | Peak crisis vintage |
| 2010 | Post-crisis tight lending |
| 2016 | Normal times |

### Columns to keep
- **Origination:** Loan Sequence Number, First Payment Date, Credit Score, Original LTV, Original CLTV, Original DTI, Original UPB, Original Interest Rate, Loan Purpose, Occupancy Status, First Time Homebuyer Flag, Number of Borrowers, Property State, Channel
- **Servicing:** Loan Sequence Number, Monthly Reporting Period, Current Actual UPB, Current Loan Delinquency Status, Loan Age, Zero Balance Code, Zero Balance Effective Date

Load one year at a time, keep only these columns, save trimmed Parquet to `data/processed/`.

---

## 2. Key definitions (decide and write these down before coding)

| Item | Working definition | Check |
|---|---|---|
| Vintage | Origination quarter from the Loan Sequence Number (e.g. `F07Q1...` -> 2007Q1). 4 years x 4 quarters = **16 vintages** | |
| Loan age / MOB | `Loan Age` field from servicing file | Spot-check vs first payment date |
| Default event | **First month** the loan is 90+ days past due (delinquency status >= 3 or `RA`), **or** it exits with a loss-type Zero Balance Code (e.g. 02, 03, 09, 15) without hitting 90+ first | Confirm ZBC values in the Freddie Mac user guide |
| Default is absorbing | Once defaulted, a loan stays defaulted (no cure counted) | |
| Prepayment event | Zero Balance Code 01 (prepaid / matured) | |
| Denominator | **Loans originated in the vintage** (count). UPB-weighted version as a second view | |
| Prepaid loans | Stay in the denominator. Prepayment is a **competing risk**, not censoring (a prepaid loan can no longer default) | Bellini 5.4 |

**Decision statement to write in the notebook:** the chosen default definition, and why 90+ DPD (matches Basel/APRA "90 days past due" backstop).

---

## Folder structure and workflow

```
Freddie Mac End-to-End Project/
├── plan.md
├── .gitignore              data/ never committed
├── data/
│   ├── raw/                sample_YYYY.zip (read straight from the zip)
│   ├── interim/            trimmed orig + perf Parquet per year   (stage 00)
│   ├── processed/          loan-month panel + loan event table    (stage 01)
│   └── dashboard/          small aggregate tables                 (stage 04)
├── notebooks/              one per stage, worked on 2007 first
│   ├── 00_load_and_trim.ipynb
│   ├── 01_build_panel.ipynb
│   ├── 02_vintage_curves.ipynb
│   ├── 03_segment_analysis.ipynb
│   └── 04_export_for_dashboard.ipynb
├── src/freddie/            functions graduate here from the notebooks
│   ├── config.py           paths, YEARS, columns, dtypes, codes, bands
│   ├── load.py             stage 00
│   ├── panel.py            stage 01
│   ├── vintage.py          stage 02
│   ├── segments.py         stage 03
│   ├── export.py           stage 04
│   └── plots.py            shared charts
├── pipeline/
│   └── run_all_years.py    loops stages 00-04 over all 4 years
├── outputs/
│   ├── figures/
│   └── tables/
└── dashboard/              stage 05
```

**Loop for each stage**
1. Work the stage in its notebook on **2007 only**.
2. Once a step works, turn it into a function in the matching `src/freddie/` module and call it from the notebook.
3. The stage is finished when the notebook is mostly function calls plus markdown and decision statements.
4. Add that stage to `pipeline/run_all_years.py` and run it for 2006, 2010 and 2016. Spot-check row counts and default rates by year.
5. Move to the next stage.

Rule of thumb: a function takes `year` (or a DataFrame) as input and has no hardcoded "2007" or file paths inside. Paths and constants live in `config.py`.

---

## 3. Notebook sequence

```
00_load_and_trim      raw .txt  ->  trimmed parquet (one year at a time)
        |
01_build_panel        loan-month panel + vintage, MOB, default/prepay flags (first event only)
        |
02_vintage_curves     cumulative default % and prepay % by vintage x MOB
        |
03_segment_analysis   curves cut by credit score, LTV, DTI, purpose, occupancy, channel, state
        |
04_export_for_dash    small aggregate tables -> data/dashboard/*.parquet
        |
05_dashboard          reads ONLY the aggregate tables
```

### 00 Load and trim
- Read with `sep="|"`, `header=None`, assign column names from the user guide.
- Set dtypes on read (categoricals for flags/state) to keep memory down.
- **Done when:** 4 orig + 4 perf Parquet files exist and row counts are logged.

### 01 Build the panel
- Join origination traits to servicing rows.
- Derive `vintage_q`, `mob`, `default_flag`, `prepay_flag`, `first_event_mob`, `first_event_type`.
- Sanity checks: one origination row per loan; no months after a loan's zero-balance date; default rate per year in a believable range (2007 high, 2016 low).
- **Done when:** one tidy panel per year, plus a loan-level table with first event type and MOB.

### 02 Vintage curves
- For each vintage and MOB: `cum_default_rate = loans defaulted by MOB / loans originated`.
- Same for prepayment. Also the marginal (monthly) default rate.
- Charts: 16 cumulative default curves; same by year (4 curves); vintage x MOB heatmap (the "triangle").
- Note **right truncation**: 2016 vintages have fewer months observed, so curves end earlier. Compare vintages at fixed MOBs (12, 24, 36, 60).
- Read first: **Bellini 3.2 and 3.4** (printed pp. 93-98, 112-126), then **5.4** for competing risks.
- **Done when:** a table of cumulative default % at MOB 12/24/36/60 for all 16 vintages, plus a written read of the curves (when do defaults peak, how far apart are 2007 and 2016).

### 03 Segment analysis
- Bands: credit score (<620, 620-679, 680-739, 740+), LTV (<=60, 60-80, 80-90, 90+), DTI (<=36, 36-43, 43+), plus purpose, occupancy, first-home buyer, channel, top states.
- Question for each cut: does the segment gap stay constant across years, or does it widen in 2006/2007? (loose underwriting showing up)
- Link to lending background: compare the US bands to how serviceability buffers, HEM and LVR/LMI thresholds would treat the same borrowers.
- **Done when:** each segment section ends with a decision/finding statement (what it means for underwriting or portfolio limits).

### 04 Export for the dashboard
- Aggregates only (the dashboard should never touch the loan-month panel):
  - `vintage_curves`: vintage_q, year, mob, segment_type, segment_value, n_orig, cum_default_rate, cum_prepay_rate, upb_weighted_default_rate
  - `vintage_summary`: one row per vintage with default % at MOB 12/24/36/60, peak marginal default MOB, avg credit score/LTV/DTI
  - `portfolio_mix`: originations by vintage x segment (counts, UPB)
- **Done when:** every dashboard chart can be drawn from these three tables.

---

## 4. Portfolio dashboard

**Audience:** a credit risk manager asking "which vintages and segments are hurting us, and is the new book better than the old book?"

### Layout
```
+------------------------------------------------------------------+
| Filters: year | vintage quarter | segment type | segment value     |
+------------------------------------------------------------------+
| KPI: loans | orig UPB | cum default % @36 | cum prepay % @36       |
+--------------------------------------+---------------------------+
| Vintage curves (cum default % by MOB) | Vintage x MOB heatmap     |
| one line per selected vintage         | (the triangle)            |
+--------------------------------------+---------------------------+
| Segment comparison                    | Default vs prepay         |
| (default % @36 by band, per year)     | (competing risks by year) |
+--------------------------------------+---------------------------+
| Vintage summary table (sortable)                                  |
+------------------------------------------------------------------+
| Findings: 3-4 plain-English takeaways + business recommendations  |
+------------------------------------------------------------------+
```

### Build decision (pick one before starting)
| Option | Pros | Cons |
|---|---|---|
| **Static Plotly HTML** on smallchuch.github.io | Free, always online, matches portfolio styling, aggregates are small enough to embed | Filtering limited to what Plotly/JS dropdowns can do |
| Streamlit (same as Flagship) | Easy filters, reuse Flagship skills | Needs hosting (Streamlit Community Cloud), sleeps when idle, styling harder to match site |

Default lean: **static Plotly HTML**, since the inputs are pre-aggregated and there is no model to run live.

- **Done when:** dashboard is live, linked from the portfolio site, and the findings panel is written.

---

## 5. Write-up
- Short README: question, data, definitions, 3-4 key findings, dashboard link.
- US vs Australia notes: 30-year fixed loans and free refinancing (high prepayment), US mortgage insurance vs LMI, no APRA serviceability buffer.
- Flag AI-assisted parts as usual.

---

## Parked (do not start until the dashboard is live)
1. **PD** model on origination traits (default = 90+ DPD).
2. **EAD:** Current Actual UPB in the month of default.
3. **LGD:** defaulted loans only, from Net Sale Proceeds, MI/Non-MI Recoveries, Expenses, Actual Loss.
4. **Lifetime PD** from the vintage curves (survival / competing risks).
5. **IFRS 9-style ECL:** staging, 12-month vs lifetime, scenario weights (2007 downside / 2010 base / 2016 upside), discounting.
