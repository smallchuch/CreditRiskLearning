# Project — Loan-Book Portfolio Dashboard (Plotly + Streamlit)

- **Module:** Credit Risk ML — Portfolio companion piece (BI / data visualisation / stakeholder storytelling)
- **Project type:** Interactive analytical dashboard + supporting design documentation
- **Dataset:** Home Credit Default Risk — `application_train.csv` (Kaggle). Same book you screened in the EDA project. Synthetic stand-in acceptable if the real file isn't to hand.
- **Estimated effort:** ~3–4 evenings (14–18 hours, including the design doc and write-up)
- **Prerequisites:** Pandas basics; the Home Credit EDA project (you should already know this book's fields and quirks); Streamlit layout model (tabs, columns, sidebar); Plotly Express basics
- **Weighting toward portfolio:** High — this is the piece that proves you can turn analysis into a **product a non-analyst can use**, and that you can scope, document, and defend a deliverable the way a team member does.

---

## 1. Overview & context

A dashboard is not "some charts in a web app." In a real credit-analytics team, a portfolio dashboard is the thing a risk committee, a lending manager, or a finance partner opens on a Monday morning to answer *"what does our book look like right now?"* — without pinging an analyst. It has to answer real questions, in the order those people think about them, fast enough that they trust it.

This project takes the Home Credit loan-book you already screened for default drivers and turns it into that product. You will build a **multi-tab Streamlit dashboard** (charts rendered with Plotly) that lets someone across the organisation get a snapshot of the book — how much is being lent, to whom, at what risk — and drill into the segments that matter.

But the dashboard is deliberately *only half the submission*. The other half is the **documentation and decision-making** around it. Anyone can wire up `st.plotly_chart`. What signals you're ready to work on a team is that you scoped the thing before building it, defined every metric precisely, chose the layout for a reason you can articulate, and left a paper trail a colleague could pick up. In BI work, wireframes are cheap; the scarce skill is the written reasoning that shows you designed for an audience and a decision — not for yourself.

Two threads run through this project on top of the build itself:

- **Design before build.** You decide what each tab is *for* and sketch the structure before writing chart code. The design doc is graded as heavily as the app. A polished dashboard with no documented reasoning reads as junior; a plain dashboard with a sharp one-page spec reads as someone who can own a deliverable.
- **Audience discipline.** The dashboard is for a *non-technical, cross-functional* audience. Every metric label, every chart, every default view is judged on whether that audience can read it unaided. Jargon, unlabelled axes, and "default rate" numbers with no base-rate context all cost marks here — the same way they'd cost you credibility in a stakeholder review.

---

## 2. Learning outcomes

On completing this project you should be able to:

1. Scope a stakeholder-facing analytical product — identify the audience, the decisions it supports, and the ranked questions it must answer — and write that scope down.
2. Design a dashboard's information architecture (tabs, sections, filters) using the inverted-pyramid principle: overview first, drill-down after.
3. Define analytical metrics precisely and unambiguously in a metric dictionary, including the credit-risk ones (default rate, exposure, PD band) that teams routinely dispute.
4. Build a multi-tab interactive dashboard in Streamlit with Plotly visualisations, correct layout, and global filtering.
5. Match chart type to question, and present each so a non-technical viewer reads the answer without help.
6. Document design decisions and hand off a repo a colleague can run and understand from the README alone.

---

## 3. The task

Build an interactive **loan-book portfolio dashboard** in Streamlit, with charts rendered in Plotly, over the Home Credit application data. It should let a cross-functional audience understand the current state of the book and drill into segments. Alongside the app, produce the **design and documentation artefacts** (Section 6) that show how you scoped and reasoned about it.

Anchor the build to the audience and questions you've already committed to in your plan:

> **Audience:** people across the organisation wanting a snapshot of the loan-book and its current state.
>
> **Questions the dashboard must answer:** how much are we lending · who are we lending to · which customers have defaulted · which customers are at highest risk · what is the credit profile of the book · what is our exposure · what are we lending against (dwelling / asset types).

Scope boundary: **this is a descriptive/monitoring dashboard, not a modelling exercise.** You may *display* risk (default flags, score/PD bands, EXT_SOURCE profiles) but you are not fitting a model here — that's the flagship PD project. If a "highest risk" view needs a score, use an existing field or a simple documented proxy, and say so.

---

## 4. Recommended app structure

Design top-down, then build bottom-up. Decide the content of each tab on paper (Section 6, design doc) **before** writing chart code. Then build the empty skeleton with placeholders, get the data layer and filters working, and fill visualisations in last — one per save.

Suggested information architecture (inverted pyramid — overview, then drill):

1. **Setup & data layer** — `set_page_config(layout="wide")` first; load data once behind `@st.cache_data`; derive the fields the tabs need (age from `DAYS_BIRTH`, PD/score band, exposure) in one documented prep step.
2. **Global sidebar filters** — the controls that apply to the *whole* book (e.g. contract type, gender, segment). Every tab reads these. Keep tab-specific controls inside their tab.
3. **Overview / KPI band** — the headline numbers a viewer wants first: total lending, customer count, overall default rate (against the ~8% base rate), total exposure. `st.metric` cards.
4. **Demographics tab** — who we lend to: age, income, family status, region, dwelling/asset type. Distributions and category breakdowns.
5. **Default tab** — which customers defaulted and how the rate moves: default rate by segment, by band, and the score/profile split between defaulters and non-defaulters.
6. **Credit tab** — the credit profile of the book: score/EXT_SOURCE distributions, exposure, utilisation/limit relationships, highest-risk drill.

Every tab should open by answering *its* headline question at a glance, then let the viewer drill. If a chart doesn't answer one of the Section 3 questions, cut it.

---

## 5. Detailed expectations

**Scope & audience, written down.** The design doc must state, in one or two sentences, who the dashboard is for and what decision/understanding it supports — then list the ranked questions and map each to the metric and chart that answers it. This is the spine of the submission.

**Metric definitions stated explicitly.** Every headline number needs a precise definition in the metric dictionary. In particular: what counts as a *default* (which flag/field, what it represents), how *exposure* is measured (`AMT_CREDIT`? outstanding?), how a *risk/PD band* is derived, and how any *rate* is computed (numerator/denominator). Ambiguous metric definitions are the number-one source of team disputes — defining them is the point.

**Base-rate discipline.** The book's overall default rate (~8%) must appear as an anchor, and every "default rate by segment" number must be readable against it. A segment rate with no base-rate reference is a mark-loser here, exactly as in the EDA project.

**Layout serves the questions.** Wide layout on. Overview KPIs before detail. Global filters in the sidebar, tab-specific controls in-tab (with unique `key=`s to avoid duplicate-widget errors). Weighted columns where a chart deserves more room than its side panel. The design doc must justify the tab split and ordering — not just describe it.

**Chart-to-question fit.** Match shape to question: distribution → histogram/box, comparison across categories → bar, part-to-whole → stacked bar, relationship → scatter, trend → line. Each chart must trace back to a Section 3 question. Decorative charts that answer nothing get cut.

**Readable for a non-technical audience.** Titled charts, labelled axes with plain-English names (not raw column names like `AMT_CREDIT`), legible number formatting (`4.2%`, `1,284`, `£1.2M`), and no unexplained credit jargon in labels. Assume the viewer has never seen the dataset.

**Performance.** Data load and any heavy derivation sit behind `@st.cache_data` so the app doesn't recompute the whole book on every filter change. The app should feel instant when a filter moves.

**Reproducible & runnable.** A colleague clones the repo, installs from `requirements.txt`, runs `streamlit run app.py`, and it works against the stated data file with no hidden manual steps.

---

## 6. Deliverables

This is the heart of the submission — the dashboard is one of several artefacts, and the documentation is weighted as heavily as the app.

- [ ] **The dashboard** (`app.py`, runnable) — multi-tab Streamlit + Plotly app answering the Section 3 questions, wide layout, global sidebar filters, cached data layer, no leftover errors.
- [ ] **Design doc / dashboard spec** (`design_doc.md`) — the scoping-and-reasoning artefact (see Section 7). Audience, decision, ranked questions → metric → chart, layout rationale, and what you deliberately left out.
- [ ] **Metric dictionary** (`metric_dictionary.md`) — every metric and derived field defined precisely: name, plain-English meaning, exact formula / source column(s), and any assumptions (what counts as default, how exposure and bands are derived).
- [ ] **Low-fidelity wireframe** — the tab/section layout sketched before building (Figma, Excalidraw, or even a photographed pen sketch). Low-fi boxes-and-labels is fine and *preferred* over a polished mockup with no reasoning. Exported as an image into the repo.
- [ ] **Data prep note** — a short section (in the README or its own file) documenting how raw `application_train.csv` becomes dashboard-ready: derived fields (age, bands, exposure), any filtering, sentinel handling (`DAYS_EMPLOYED == 365243`), carried over from your EDA.
- [ ] **Decisions-first README** (`README.md`) — the repo front door: the problem, the audience, how to run it (install + command), a screenshot or two, and the 5–8 key design decisions you made and why. This is the document a hiring manager actually reads.
- [ ] **`requirements.txt`** — pinned dependencies so the app runs on a clean machine.
- [ ] *(Nice-to-have)* **A short demo** — 3–5 screenshots or a 20–30s screen-recording / GIF of the dashboard in use, embedded in the README. Makes the piece legible to someone who won't clone it.

---

## 7. The design doc (the artefact that carries this project)

The design doc is where you prove you can *scope and reason about a deliverable*, not just build one. Treat it as the document you'd hand a stakeholder before writing a line of app code. Aim for one to two pages. It should contain:

- **Purpose & audience.** One or two sentences: who opens this, and what they decide or understand from it. (You've drafted this already — sharpen it.)
- **Ranked questions.** The 5–8 questions the dashboard answers, in priority order, phrased as real questions. Anything that doesn't tie to the purpose gets cut, visibly.
- **Question → metric → chart map.** A table: each question, the specific metric/field that answers it, whether the data actually supports it, and the chart type chosen. This single table is the strongest signal in the whole submission — it shows you designed content-first.
- **Information architecture.** Why these tabs, in this order; what lives in the sidebar vs in-tab; how the inverted pyramid (overview → drill) is realised. Justify the structure, don't just describe it.
- **Metric definitions** (or a pointer to the metric dictionary) for anything ambiguous — especially default, exposure, and risk bands.
- **Explicit non-goals.** What you deliberately left out and why (e.g. "no PD model here — this is descriptive; risk shown via existing scores"). Naming your scope boundaries reads as senior.
- **Validation.** A short reflection: can the target viewer answer each ranked question quickly? What earned its place, what didn't?

The discipline being assessed is the same as the EDA project's audit trail: a colleague who doesn't know you should be able to read this doc and understand *why the dashboard is shaped the way it is* — before they ever open the app.

---

## 8. Rules & constraints

- **Design before charts.** The design doc's question→metric→chart map should exist before the app is built. Don't reverse-engineer it after the fact — it shows.
- **Descriptive, not predictive.** No model fitting in this project. Display risk via existing fields or a documented proxy; modelling is the flagship piece.
- **State your definitions.** Default, exposure, risk band, and every rate — defined explicitly in the metric dictionary, no silent conventions.
- **Every chart earns its place.** If a visual doesn't answer a ranked question, remove it. A tight dashboard beats a busy one.
- **Non-technical audience throughout.** Plain-English labels, no raw column names on the page, base rate always in view for default figures.
- **No placeholder text in the final version.** README, design doc, and metric dictionary must contain real content, not template stubs.

---

## 9. Marking rubric

Australian grading bands. Criteria weightings sum to 100. Note that **documentation and design carry 45 of the 100 marks** — this is a communication-and-judgment piece as much as a build.

| Criterion | Weight | High Distinction (85–100) | Credit–Distinction (65–84) | Pass (50–64) | Fail (<50) |
|---|---|---|---|---|---|
| **Scope & design doc** | 20 | Audience and decision crisp; ranked questions each mapped to metric + chart; layout justified; non-goals named; a colleague could build from it | Solid scope and question→chart map; rationale present but thin in places | Doc exists but scope vague or map incomplete | No design doc, or purely descriptive with no reasoning |
| **Metric dictionary & definitions** | 12 | Every metric precisely defined with formula/source and assumptions; default, exposure, bands unambiguous | Most metrics defined; a couple loose or missing an assumption | Some definitions, but key ones (default/exposure) ambiguous | No usable definitions |
| **Information architecture & layout** | 15 | Inverted pyramid realised; sensible tab split; global vs in-tab controls right; wide layout; nothing wasted | Clear structure with minor layout awkwardness | Works but cluttered or mis-ordered (detail before overview) | Disorganised; viewer can't navigate |
| **Chart choice & correctness** | 15 | Every chart fits its question and is computed correctly against the base rate; no decorative filler | Mostly good fit; a slip in one chart type or a rate not base-rate-anchored | Charts present but some mismatched or miscomputed | Wrong or meaningless visuals |
| **Stakeholder readability** | 15 | Plain-English labels, formatted numbers, no raw column names or jargon; a non-analyst reads every answer unaided | Mostly readable; a chart or two too technical | Assumes dataset knowledge; unlabelled axes | Unreadable for the stated audience |
| **Interactivity & performance** | 10 | Global filters work across tabs; cached data layer; feels instant; no duplicate-widget bugs | Filters work; minor lag or a stray uncached path | Filtering partial or app recomputes everything | Filters broken or app unusably slow |
| **README & reproducibility** | 8 | Clone → install → run works first time; README states problem, audience, run steps, key decisions, screenshot | Runs with minor friction; README mostly complete | Runs only with undocumented steps; thin README | Doesn't run / no README |
| **Code quality** | 5 | Clean, sensible names, prep isolated and documented, no dead cells | Runs with minor untidiness | Messy or fragile | Broken |

**Grade bands:** HD ≥ 85 · D 75–84 · Cr 65–74 · P 50–64 · Fail < 50.

---

## 10. Common pitfalls (learn from these before you start)

- **Building charts before scoping.** Jumping to `st.plotly_chart` before the question→metric→chart map means you shuffle working chart code between tabs later. Design the frame first.
- **Everything centred in the middle.** The default narrow layout — fix it with `st.set_page_config(layout="wide")` as the *first* Streamlit command.
- **Default rate with no base rate.** A "6% default" segment number is meaningless without the ~8% book rate beside it. Always anchor.
- **Raw column names on the page.** `AMT_CREDIT` and `DAYS_BIRTH` are fine in code, not on a stakeholder chart. Relabel to "Loan amount" and "Age".
- **Duplicate widgets across tabs.** Same-labelled sliders in two tabs throw a duplicate-key error — give each a unique `key=`.
- **No caching.** Without `@st.cache_data`, the whole book reloads on every filter move and the app crawls. Cache the load and derivation.
- **Undefined "default" / "exposure".** If your dictionary doesn't pin these down, two viewers read two different books. Define them.
- **A polished Figma mockup with no written reasoning.** Reads as *less* professional than a rough sketch plus a sharp design doc. Invest in the reasoning, not the pixels.
- **Charts that answer nothing.** A pretty visual that maps to none of the ranked questions is clutter. Cut it.

---

## 11. Stretch goals (optional — for a comfortable HD)

- **Highest-risk drill-down** — a filtered table or view of the riskiest segment (by existing score/band), with the caveat that it's descriptive, not a model output.
- **Cross-filtering polish** — a segment control that refines multiple tabs consistently, demonstrating the shared-filter pattern cleanly.
- **A heatmap** — 2-D default rate across two dimensions (e.g. age band × income band) where it genuinely aids reading.
- **Deploy it** — push to Streamlit Community Cloud and put the live link in the README. A hiring manager clicking a working link beats a screenshot.
- **Theming** — a light custom theme (`.streamlit/config.toml`) so it looks like a product, not a default demo.
- **Data-dictionary link-through** — surface the metric definition in-app (tooltip or an expander) so the dashboard documents itself.

---

*When you're done, bring the **app, the design doc, and the metric dictionary** back and I'll mark all three against Section 9, with banded feedback per criterion. Remember: on this project the documentation is worth as much as the build — that's the point of the piece.*
