# Streamlit + Plotly Dashboard Cheat Sheet

A single-page reference for building a credit-risk portfolio dashboard.
**Division of labour:** Streamlit = *where things go* (page, tabs, layout, widgets). Plotly = *what the charts look like*.

---

## 0. Setup & Running

```bash
pip install streamlit plotly pandas
streamlit run app.py          # start the app (opens http://localhost:8501)
```

Dev loop: **edit → save → the browser shows "Rerun" (click "Always rerun" once).**
Stop the server: **Ctrl+C** in the terminal. Port stuck? `lsof -ti:8501 | xargs kill` (mac/linux).

Standard import block at the top of every app:

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
```

---

## 1. Page Structure

### Page config — always first Streamlit command
```python
st.set_page_config(
    page_title="Portfolio Analysis",
    layout="wide",            # <-- fixes the "everything's in the middle" default
    initial_sidebar_state="expanded",
)
```

### Tabs — the top-level split for your dashboard
```python
tab_demo, tab_default, tab_credit = st.tabs(["Demographics", "Default", "Credit"])

with tab_demo:
    st.header("Demographics")
    # ...demographics content

with tab_default:
    st.header("Default")
    # ...default content

with tab_credit:
    st.header("Credit")
    # ...credit content
```
- List order = left-to-right tab order.
- Content goes **inside** each tab via a `with` block.
- All tabs' code runs on every rerun (inactive ones are just hidden).

---

## 2. Layout — arranging elements

Streamlit is a **vertical flow**, not a true grid. Elements stack top-to-bottom (implicit "rows"). You add horizontal structure with `st.columns()`.

### Columns (side-by-side "row")
```python
c1, c2, c3 = st.columns(3)            # equal thirds
c1.metric("Default rate", "4.2%")
c2.metric("Defaults", "1,284")
c3.metric("Avg PD", "3.8%")

left, right = st.columns([2, 1])      # weighted: left twice as wide
with left:
    st.write("wide chart")
with right:
    st.write("side panel")
```
Call `st.columns()` again each time you want a new horizontal band.

### Sidebar (controls / filters)
```python
with st.sidebar:
    st.header("Filters")
    segment = st.selectbox("Segment", ["All", "Retail", "SME"])
# or inline: st.sidebar.selectbox(...)
```

### Containers & expanders
```python
with st.container(border=True):       # visually boxed group
    st.write("grouped content")

with st.expander("Show details"):     # collapsible section
    st.write("hidden until clicked")
```

**Layout mental model:** rows = vertical order (implicit), columns = explicit `st.columns()`, arrange by *nesting* containers — no x/y coordinates.

---

## 3. Text & Display

```python
st.title("Portfolio Analysis")        # biggest
st.header("Default")                  # section
st.subheader("By segment")            # sub-section
st.write("anything — text, df, fig")  # smart, auto-detects type
st.markdown("**bold**, `code`, etc.") # full markdown
st.caption("small grey note")
st.divider()                          # horizontal rule
```

---

## 4. Input Widgets

Each widget returns its current value as a plain variable. The script reruns when it changes.

```python
seg   = st.selectbox("Segment", ["Retail", "SME", "Corporate"])
regs  = st.multiselect("Regions", ["N", "S", "E", "W"], default=["N"])
score = st.slider("Score cutoff", 300, 850, 600)
rng   = st.slider("PD range", 0.0, 1.0, (0.1, 0.5))   # returns a tuple
on    = st.checkbox("Only defaulters")
pick  = st.radio("View", ["Count", "Rate"], horizontal=True)
date  = st.date_input("As of")
text  = st.text_input("Customer ID")
```

Usage pattern: **widget → variable → filter your DataFrame → build chart.**
```python
filtered = df[(df.segment == seg) & (df.score >= score)]
```

---

## 5. KPIs & Data Display

```python
st.metric("Default rate", "4.2%", delta="-0.3%")   # delta shows red/green arrow

st.dataframe(df, use_container_width=True)          # interactive table (sort/scroll)
st.table(df.head())                                 # static table
st.json(some_dict)                                  # pretty JSON
```

---

## 6. Caching — keep it fast

Expensive data loads / model scoring should run once, not on every widget click.

```python
@st.cache_data
def load_data(path):
    return pd.read_csv(path)          # only re-runs if `path` changes

df = load_data("portfolio.csv")
```
Use `@st.cache_data` for data/DataFrames. (`@st.cache_resource` is for models/DB connections.)

---

## 7. Plotly — the charting half

**The handoff is always two lines:** build a figure, then hand it to Streamlit.
```python
fig = px.histogram(df, x="credit_score")
st.plotly_chart(fig, use_container_width=True)      # use_container_width=True fills the column
```

Start with **Plotly Express (`px`)** — every chart is a one-liner. Common arguments across all of them:
`x`, `y`, `color` (split by category), `title`, `labels={...}`, `barmode`, `nbins`.

### The 5 chart types that cover a portfolio dashboard

```python
# Histogram — distributions (scores, age, income)
px.histogram(df, x="credit_score", nbins=40, color="segment")

# Bar — rates / counts by category (default rate by region)
px.bar(df_grouped, x="region", y="default_rate", color="region")

# Line — trends over time (default rate by vintage/month)
px.line(df_ts, x="month", y="default_rate", color="segment")

# Scatter — relationships (income vs limit, score vs PD)
px.scatter(df, x="income", y="credit_limit", color="default_flag", size="exposure")

# Box — spread & outliers (score distribution by default status)
px.box(df, x="default_flag", y="credit_score")
```

### Styling you'll actually use
```python
fig.update_layout(title="Score distribution", xaxis_title="Score",
                  yaxis_title="Count", showlegend=True, height=400)
fig.update_traces(marker_color="steelblue")
```

Drop to `plotly.graph_objects` (`go`) only when Express can't express it (e.g. a custom ROC curve — see below).

---

## 8. Chart-to-Tab Map (credit-risk portfolio)

| Tab | What to show | Chart |
|-----|--------------|-------|
| **Demographics** | Age / income distribution | `px.histogram` |
| | Customers by region/segment | `px.bar` |
| | Income vs credit limit | `px.scatter` |
| **Default** | Default rate by segment/region | `px.bar` |
| | Default rate over time (vintage) | `px.line` |
| | Score by default status | `px.box` |
| | KPI cards (rate, count, avg PD) | `st.metric` |
| **Credit** | Credit score distribution | `px.histogram` |
| | Utilisation vs limit | `px.scatter` |
| | Score buckets (band counts) | `px.bar` |

### ROC / AUC curve (uses `graph_objects`)
```python
from sklearn.metrics import roc_curve, auc
fpr, tpr, _ = roc_curve(y_true, y_scores)
fig = go.Figure()
fig.add_trace(go.Scatter(x=fpr, y=tpr, name=f"ROC (AUC={auc(fpr, tpr):.2f})"))
fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], line=dict(dash="dash"), name="Random"))
fig.update_layout(xaxis_title="False Positive Rate", yaxis_title="True Positive Rate")
st.plotly_chart(fig, use_container_width=True)
```

---

## 9. Full Skeleton — everything wired together

```python
import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Portfolio Analysis", layout="wide")

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data("portfolio.csv")

# ---- Sidebar filters ----
with st.sidebar:
    st.header("Filters")
    seg = st.selectbox("Segment", ["All"] + sorted(df.segment.unique()))

view = df if seg == "All" else df[df.segment == seg]

# ---- Tabs ----
st.title("Portfolio Analysis")
tab_demo, tab_default, tab_credit = st.tabs(["Demographics", "Default", "Credit"])

with tab_demo:
    st.header("Demographics")
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.histogram(view, x="age", nbins=30), use_container_width=True)
    c2.plotly_chart(px.histogram(view, x="income", nbins=30), use_container_width=True)

with tab_default:
    st.header("Default")
    a, b, c = st.columns(3)
    a.metric("Default rate", f"{view.default_flag.mean():.1%}")
    b.metric("Defaults", f"{int(view.default_flag.sum()):,}")
    c.metric("Customers", f"{len(view):,}")
    st.plotly_chart(px.box(view, x="default_flag", y="credit_score"),
                    use_container_width=True)

with tab_credit:
    st.header("Credit")
    st.plotly_chart(px.histogram(view, x="credit_score", nbins=40),
                    use_container_width=True)
```

---

## Quick Reference Links
- Streamlit API reference — https://docs.streamlit.io/develop/api-reference
- Streamlit cheat sheet — https://docs.streamlit.io/develop/quick-reference/cheat-sheet
- Plotly Express — https://plotly.com/python/plotly-express/
- Plotly Python (all charts) — https://plotly.com/python/

**One-sentence summary:** `set_page_config(layout="wide")` → `st.tabs()` → inside each tab use `st.columns()` + widgets → filter your DataFrame → build a `px` figure → `st.plotly_chart(fig, use_container_width=True)`.
