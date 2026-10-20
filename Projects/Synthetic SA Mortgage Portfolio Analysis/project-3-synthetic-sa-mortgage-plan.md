# Project 3: Synthetic SA Mortgage Portfolio, Stress Testing and Scenario Analysis

Last updated: 2026-10-20
Folder (laptop): `C:\Dev\CreditRiskLearning\Projects\Synthetic SA Mortgage Portfolio Analysis`
Starts: after the Freddie Mac vintage analysis + dashboard. Bulk of the build during leave.

---

## 1. The pitch

A Big 4 style engagement for a fictional metro Adelaide mortgage lender. The board risk committee asks: *"Where is our book concentrated, and what happens to arrears and losses if rates, unemployment or house prices move?"* The deliverable is a Streamlit dashboard (overview, concentration maps, animated scenario playback, a scenario lab with sliders) plus a short methodology and assumptions note.

**Framing (important):** the data is synthetic, so the project demonstrates a **stress-testing method**, not discoveries. Credibility comes from (a) calibrating the generator to public ABS / RBA / APRA / Valuer-General data, (b) calibrating the engine so the base scenario matches published arrears levels, and (c) a written assumptions register with sensitivity analysis. **No employer data, internal benchmarks or policy settings, even loosely.** Public sources only.

---

## 2. Decisions locked (2026-10-20)

| Topic | Decision |
|---|---|
| Audience | Big 4 advisory framing; imagined reader is a board risk committee |
| Book size | ~50,000 loans |
| Geography | Metro Adelaide only (Greater Adelaide). Each loan tagged with suburb + postcode. **Maps at postcode** (enough loans per area for stable colours); suburb as drill-down; macro drivers (unemployment) at SA3/SA4, passed down to postcodes |
| Book features | Owner-occupier vs investor, P&I vs interest-only, fixed vs variable (with fixed expiry date), first home buyer flag, LMI flag, LVR, DTI, origination date |
| Time | Portfolio snapshot at a reporting date, projected **quarterly over 3 years** (12 animation frames). No synthetic history |
| Engine | **Bottom-up borrower cash-flow simulation (double trigger)**: cash-flow shock causes arrears; thin/negative equity turns default into loss. Calibrated to published arrears |
| Scenarios | APRA style: base, upside, downside, severe-but-plausible; plus custom scenarios from sliders |
| ECL | Stretch. Simplified "IFRS 9-style ECL": PD from simulation, EAD from balance schedule, LGD from a formula, rule-based staging, judgment scenario weights |
| Dashboard | Streamlit (reuse the Flagship dashboard framework: config, engine, tests, UI display only) |

---

## 3. Scope

### MVP
1. **Synthetic loan book** calibrated to public data (section 5).
2. **Scenario engine** (section 6) with the four preset scenarios.
3. **Calibration** of the base scenario to published arrears + a small sensitivity table.
4. **Streamlit app:**
   - Board overview page
   - Concentration maps (static choropleths)
   - Scenario playback (animated choropleth + time-series lines)
   - **Scenario lab**: user sets parameters with sliders, engine re-runs, animation plays
   - Methodology and assumptions page

### Stretch (in priority order)
1. IFRS 9-style ECL with staging, probability-weighted across scenarios
2. Management-action scenario (e.g. raise serviceability buffer for new lending, concentration limit)
3. Regional shock scenario (large employer closure in one SA3/SA4)
4. Short engagement-style report with recommendations (export from Claude Docs or Quarto)

---

## 4. Scenario lab design (sliders)

- **Presets are precomputed** and load instantly. The board overview and playback pages use presets only, so they never break.
- **Scenario lab re-runs the engine live.** 50k loans x 12 quarters = 600k loan-quarters; a vectorised numpy/pandas engine should run in a few seconds. Wrap in `st.cache_data` keyed on the slider values. Fixed random seed so the same inputs give the same answer.
- **Sliders shape a path, not 12 numbers each:** peak cash rate change, peak unemployment change, peak house price fall, quarter of the peak, recovery speed. A helper turns these into quarterly paths.
- **Constrain slider ranges** to plausible values (e.g. unemployment +0 to +6 pp) so users can't create nonsense.
- Show the chosen scenario next to the nearest preset ("your scenario sits between downside and severe").
- **Design rule this forces early:** the engine must be a pure function, `run(book, scenario_path, params) -> panel`, with no notebook state. Build it as a module from day one, test it, and have notebooks call it.

---

## 5. Data sources (verify each when sourcing)

| Need | Source | Level |
|---|---|---|
| Boundaries | ABS ASGS: Suburbs and Localities (SAL), Postal Areas (POA), SA2/SA3/SA4, Greater Capital City (GCCSA) | Shapefile / GeoPackage |
| Where mortgaged households are, income, repayments, dwelling type | ABS Census (latest released) by POA / SAL | Postcode / suburb |
| House prices | SA Valuer-General quarterly median house sales by suburb (data.sa.gov.au, from 2011) | Suburb |
| Unemployment | ABS Labour Force detailed (SA4); Jobs and Skills Australia Small Area Labour Markets (SA2) | SA4 / SA2 |
| Rates | RBA cash rate target and housing lending rates | National |
| Book mix (LVR, DTI, IO, investor, fixed share) | APRA quarterly ADI property exposures | National / ADI |
| Arrears calibration targets | RBA Financial Stability Review; S&P SPIN (RMBS arrears by state); APRA | National / state |
| Living expenses | Public alternative to HEM (HEM itself is licensed): ABS household expenditure or a documented rule by household size/income | Assumption |

---

## 6. Design

### 6a. Loan book generator (one row per loan)

| Field | How generated |
|---|---|
| `loan_id`, `suburb`, `postcode`, `sa3`, `sa4` | Suburb drawn with weights from Census mortgaged-household counts; concordance gives postcode/SA3/SA4 |
| `property_value_orig` | Suburb median at origination quarter x lognormal dispersion |
| `orig_date`, `seasoning` | Distribution weighted to recent years (APRA new lending flow) |
| `ltv_orig`, `lmi_flag` | LVR distribution from APRA mix; LMI if LVR > 80% |
| `loan_amount`, `balance_now` | Value x LVR; balance from amortisation to the reporting date |
| `income`, `dti` | Correlated with suburb income and loan size; check DTI mix vs APRA |
| `occupancy` (OO/INV), `fhb_flag` | APRA shares; FHB more likely high LVR, outer suburbs |
| `repayment_type` (P&I/IO), `io_expiry` | IO mostly investor |
| `rate_type`, `fixed_expiry`, `rate_now` | Fixed share and expiry dates; rate = cash rate + margin |
| `term`, `household_size`, `living_expenses` | Assumption-driven |
| `offset_buffer` | Months of repayments held; skewed (many near zero) |

Correlations built by **conditional generation** (suburb → value → LVR → income), with a Gaussian copula only if the marginals look wrong.

### 6b. Scenario engine (quarterly, vectorised)

Per loan per quarter:
1. **Rate**: variable loans follow cash rate + margin; fixed loans reset at `fixed_expiry`; IO converts to P&I at `io_expiry`. Recompute repayment.
2. **Job loss**: random draw at the loan's SA4 unemployment rate path (with a duration/recovery rule).
3. **Surplus** = income (reduced if unemployed) - living expenses - repayment.
4. **Buffer**: negative surplus draws down the offset buffer; positive surplus rebuilds slowly.
5. **Arrears state**: current → 30 → 60 → 90+ when buffer is exhausted and surplus negative; cure probability back to current.
6. **Refinance / prepay**: hazard rises when the borrower can refinance (passes serviceability at the market buffer, LVR under 80%). Borrowers who fail serviceability are **mortgage prisoners**. Gives adverse selection over time.
7. **House prices**: suburb value follows the regional HPI path → current LVR.
8. **Default and loss**: 90+ = default. Loss = max(0, balance + costs - value x (1 - forced-sale discount) - LMI recovery).

Output: a loan x quarter panel → aggregates (section 7).

### 6c. Scenarios

| Scenario | Cash rate | Unemployment | House prices |
|---|---|---|---|
| Base | Flat to mild easing | Stable | Modest growth |
| Upside | Easing | Falls slightly | Stronger growth |
| Downside | Rises | Rises moderately | Falls |
| Severe | Rises sharply | Rises sharply | Falls sharply |

Exact paths set in `config/scenarios.json`, anchored on APRA / RBA published stress scenarios where available. Optional regional shock overlays one SA3/SA4.

### 6d. Calibration

Tune a small set of free parameters (cure rate, job-loss-to-arrears link, buffer behaviour, refinance hazard) so the **base scenario** reproduces published SA / national arrears levels. Record each parameter and its source or judgment in the assumptions register. Sensitivity table: change each key parameter +/- and show the downside loss change.

---

## 7. Outputs (what the app reads)

Aggregate tables only (the app never loads the loan panel for presets):
- `postcode_quarter_scenario`: loans, balance, 30+ rate, 90+ rate, defaults, loss, avg current LVR
- `portfolio_quarter_scenario`: the same at portfolio level, plus by segment (OO/INV, FHB, fixed expiring, high LVR)
- `concentration`: share of balance by postcode, top-10 postcode share, HHI, high-LVR / investor / IO / fixed-expiring-in-12m shares by postcode
- Simplified boundaries (`shapely` simplify) to keep the app light

---

## 8. Dashboard pages

| Page | What the board sees |
|---|---|
| 1 Overview | Headline numbers per scenario (90+ arrears peak, defaults, loss), traffic lights vs illustrative risk appetite limits, one map, three plain-English key messages |
| 2 Concentration | Choropleths: exposure, high LVR, investor share, fixed expiring in next 12 months; top-10 postcodes table |
| 3 Scenario playback | Pick a preset, press play: animated postcode map + portfolio lines by scenario |
| 4 Scenario lab | Sliders → live run → animation; compared with nearest preset |
| 5 Methodology | Method in plain words, assumptions register, sensitivity table, limitations |
| 6 ECL (stretch) | Stage mix, ECL by scenario, probability-weighted ECL |

---

## 9. Folder structure (mirrors the Flagship dashboard framework)

```
Synthetic SA Mortgage Portfolio Analysis/
  config/      scenarios.json, params.json, risk_appetite.json, slider_ranges.json
  data/raw/    downloads (ABS, RBA, APRA, Valuer-General)
  data/processed/  cleaned inputs, loan_book.parquet, aggregates
  sa_engine/   generator.py, paths.py (slider → path), engine.py, aggregate.py
  notebooks/   (section 10)
  app/         Streamlit pages, theme
  tests/       engine determinism, conservation (balances add up), monotonicity (worse scenario → more arrears), slider ranges
  docs/        assumptions register, methodology
```

---

## 10. Notebook sequence

| # | Notebook | Output |
|---|---|---|
| 00 | Data sourcing | Raw files + source log |
| 01 | Geography | Metro boundaries, suburb → postcode → SA3/SA4 concordance |
| 02 | Loan book generator | `loan_book.parquet` + checks vs APRA/Census marginals |
| 03 | Book EDA and concentration | Concentration metrics + first maps |
| 04 | Scenarios | Scenario paths + slider path helper |
| 05 | Engine | Engine module tested on a small sample, then full book |
| 06 | Calibration and sensitivity | Tuned params + sensitivity table |
| 07 | Aggregates export | Tables the app reads |
| App | Streamlit | Pages 1 to 5 |
| 08 | ECL (stretch) | Staging + weighted ECL |
| 09 | Report (stretch) | Engagement-style write-up |

---

## 11. Assumptions register (skeleton)

| ID | Assumption | Value | Source / judgment | Sensitivity tested? |
|---|---|---|---|---|
| A1 | Living expenses rule | | | |
| A2 | Job loss draw follows SA4 unemployment path | | | |
| A3 | Cure probability from 30+ | | | |
| A4 | Refinance hazard and serviceability buffer | | | |
| A5 | Forced-sale discount | | | |
| A6 | LMI recovery share | | | |
| A7 | Scenario weights (stretch) | | | |

---

## 12. Watch-outs

- Circularity: say plainly that relationships are assumed and calibrated, not discovered.
- Keep it fully separate from work data.
- Map noise: postcodes with few loans; set a minimum count or grey them out.
- Streamlit Community Cloud memory: presets as aggregates; live lab runs on the 50k book only.
- Determinism: fixed seed everywhere; tests check identical output for identical inputs.

---

## 13. Open questions

- Leave dates (to plan phases against)
- Illustrative risk appetite thresholds for the traffic lights
- Scenario weights for the stretch ECL
- Reporting date for the snapshot (suggest latest quarter with Valuer-General data)
