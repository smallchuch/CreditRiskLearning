"""Applicant PD dashboard (Streamlit). Written by AI.

Run from the 05_Applicant_PD_Dashboard folder:
    streamlit run pd_app/app.py

Layout: result panel across the top, applicant form underneath, model notes
collapsed at the bottom. Styling lives in theme.py (matches the portfolio site).
The page only collects answers and displays results. All rules live in
config/*.json, all maths in shared_stage.py and the model adapters.

    form -> validate -> engineer -> registry.score_all -> result panel
"""
import streamlit as st

import registry
import shared_stage as ss
import theme

st.set_page_config(page_title="Applicant PD | Chuch", page_icon="📊", layout="wide")
theme.inject()


# ---------------------------------------------------------------- config ---
@st.cache_data
def cfg(name):
    return ss.load_config(name)


emp = cfg("employment_rules")
loan = cfg("loan_terms")
ext = cfg("ext_score_bands")
area = cfg("area_rating_options")
notes = cfg("model_notes")["known_limitations_to_disclose"]
base_rate = cfg("portfolio_stats")["in_policy_default_rate"]

income_types = list(emp["income_types"]) + list(emp["out_of_policy"]["income_types"])
org_labels = [o["label"] for o in cfg("organisation_options")["options"]]
occ_labels = cfg("occupation_options")["options"]
edu_labels = [o["label"] for o in cfg("education_options")["options"]]
area_values = [o["value"] for o in area["options"]]
area_names = {o["value"]: o["label"] for o in area["options"]}
t = loan["term_months"]
terms = list(range(t["min"], t["max"] + 1, t["step"]))
rate = loan["repayment"]["assumed_rate_pa"]

ext_bands = ext["fields"]["EXT_SOURCE_1"]["bands"]
ext_options = [b["label"] for b in ext_bands] + [ext["missing_label"]]
ext_ranges = {b["label"]: b["score_range"] for b in ext_bands}


def ext_display(label):
    return f"{label} ({ext_ranges[label]})" if label in ext_ranges else label


def money(x):
    return f"${x:,.0f}"


# ------------------------------------------------------------------ hero ---
theme.hero(
    "Flagship PD Model · Applicant scoring",
    'Applicant <span class="accent">PD</span> dashboard',
    "Enter an applicant and a cash loan to see the scorecard's estimated probability "
    "of payment difficulty. Illustrative portfolio model trained on Home Credit data.",
)

result_slot = st.container()          # filled after the form is submitted

# ------------------------------------------------------------------ form ---
with st.form("applicant"):
    c1, c2, c3 = st.columns(3, gap="large")

    with c1:
        theme.kicker("Applicant")
        income_type = st.selectbox("Income type", income_types)
        a1, a2 = st.columns(2)
        age = a1.number_input("Age", min_value=18, max_value=75, value=35)
        employment_years = a2.number_input("Years employed", min_value=0.0,
                                           max_value=55.0, value=5.0, step=0.5,
                                           format="%.1f")
        occupation = st.selectbox("Occupation", occ_labels)
        org_option = st.selectbox("Organisation type", org_labels)
        education = st.selectbox("Highest education", edu_labels)

    with c2:
        theme.kicker("Credit history")
        ext_1 = st.selectbox("Credit score 1", ext_options, index=2, format_func=ext_display)
        ext_2 = st.selectbox("Credit score 2", ext_options, index=2, format_func=ext_display)
        ext_3 = st.selectbox("Credit score 3", ext_options, index=2, format_func=ext_display)
        area_rating = st.selectbox(area["form_label"], area_values,
                                   index=area_values.index(area["default"]),
                                   format_func=area_names.get)

    with c3:
        theme.kicker("Cash loan")
        loan_amount = st.number_input("Loan amount ($)", min_value=10_000,
                                      max_value=4_000_000, value=500_000, step=10_000)
        goods_price = st.number_input("Goods price ($)", min_value=10_000,
                                      max_value=4_000_000, value=500_000, step=10_000)
        term_months = st.selectbox("Term (months)", terms, index=terms.index(36))
        st.write("")
        submitted = st.form_submit_button("Score applicant", type="primary")

form = {
    "income_type": income_type, "age": age, "employment_years": employment_years,
    "org_option": org_option, "occupation": occupation, "education": education,
    "area_rating": area_rating,
    "ext_1_band": ext_1, "ext_2_band": ext_2, "ext_3_band": ext_3,
    "loan_amount": loan_amount, "term_months": term_months, "goods_price": goods_price,
}

notes_box = st.container()            # model notes always sit at the very bottom


def show_notes(row=None):
    with notes_box:
        if row is not None:
            with st.expander("What the model saw"):
                st.dataframe(row.T.rename(columns={0: "value"}).astype(str))
        with st.expander("About this model"):
            for n in notes:
                st.markdown(f"- {n}")


# ------------------------------------------------------------- scoring ---
with result_slot:
    if not submitted:
        theme.empty_result("Fill in the applicant below and press <b>Score applicant</b>.")
        show_notes()
        st.stop()

    theme.scroll_to_top()             # any submission: bring the top panel into view

    # 1. Policy: out-of-policy applicants are never scored
    if income_type in emp["out_of_policy"]["income_types"]:
        st.error(emp["out_of_policy"]["message"])
        st.caption(emp["out_of_policy"]["income_types"][income_type])
        show_notes()
        st.stop()

    # 2. Validation: errors block, warnings are shown
    errors, warnings = ss.validate(form)
    for e in errors:
        st.error(e)
    if errors:
        show_notes()
        st.stop()
    for w in warnings:
        st.warning(w)

    # 3. Score with every model in the registry (champion first)
    row = ss.engineer(form)
    results = registry.score_all(row)
    champ, others = results[0], results[1:]

    if "error" in champ:
        st.error(f"Champion model could not score: {champ['error']}")
        show_notes(row)
        st.stop()

    # 4. Plain-language loan figures
    monthly = ss.repayment(loan_amount, term_months)
    stats = [
        (money(monthly), "Monthly repayment"),
        (money(monthly * term_months), f"Total repaid over {term_months} months"),
        (f"{loan_amount / goods_price:.0%}", "Loan as % of goods price"),
    ]

    # 5. How this PD compares with the in-policy training population
    ratio = champ["pd"] / base_rate
    pill = "safe" if ratio < 1 else ("watch" if ratio < 1.5 else "bad")
    pill_text = f"{ratio:.1f}× the in-policy average ({base_rate:.1%})"

    chal_html = ""
    if others:
        chips = "".join(
            f'<div class="chal">{r["model"]} v{r["version"]}<br>'
            + (f'<b>{r["pd"]:.1%}</b>' if "error" not in r else "could not score")
            + "</div>" for r in others)
        chal_html = f'<div class="challengers">{chips}</div>'

    model_line = (f'<b>Champion</b> · {champ["model"]} v{champ["version"]} · '
                  f'Test Gini {champ["test_gini"]:.2f} · {champ["calibration"]} · '
                  f'{rate:.0%} p.a. illustrative rate · amounts in dataset currency units')

    theme.result_panel(f'{champ["pd"]:.1%}', pill, pill_text, stats, model_line, chal_html)

show_notes(row)
