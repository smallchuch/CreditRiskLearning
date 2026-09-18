# Handoff — Finishing the Default-Rate Driver Scan → Modelling

_Roadmap to take the Flagship PD project from where it stands now (EDA through 3.4 complete) to a finished screening deliverable and the start of modelling. Companion to `Explanation Materials/default_rate_driver_scan_walkthrough_log.md`, which holds the per-section reasoning._

---

## 1. Where the notebook stands

**Done + documented** (walkthrough log complete for these):
- Project Setup, §1 First Look, §2 Data Quality & Missingness (2.1–2.4), §3 Feature Analysis families **3.1 External Scores, 3.2 Loan Financials, 3.3 Age & Employment, 3.4 Key Demographics**.
- Notebook fixes applied this session: `SK_ID_CURR` typed as `id`; bar-label unit bugs; `Prediction:`→`Explanation:` relabel; ORG_BAND leakage note + refit-in-5.1 caveat; OCCUPATION pooling threshold 5%; added Score Intercorrelation code; colour-blind-safe palette on the EXT overlay; all §3 Observation/Decision cells written.

**Stubbed / to build:**
- **3.5 Other Numericals** — headers + empty Observation cells only.
- **§4 Feature Engineering** — 4.1 ratios defined (code exists), 4.2 sanity-check skeleton, 4.3/4.4 empty.
- **§5 WOE/IV** — split written, `calc_woe_iv` helper written; 5.3–5.6 mostly empty.
- **§6 Findings, §7 Next Steps, §8 Assumptions** — placeholders.

---

## 2. Carry-forward decisions (the spec for Section 5 binning)

Everything below was decided during the walkthrough. This table *is* the binning plan — Section 5 should implement it.

| Family / feature | Treatment for WOE/IV | Notes |
|---|---|---|
| `EXT_SOURCE_1/2/3` | Quantile bins; **missing = its own bin** | Strongest drivers (Gini 0.31–0.36). Missingness is informative (esp. _1 at 56%). Check intercorrelation before keeping all three. |
| `AMT_INCOME/CREDIT/ANNUITY/GOODS_PRICE` | Quantile bins; expect **low IV** | Weak, non-monotonic as raw amounts. No log needed (quantiles are rank-invariant). Real signal is the §4 ratios. |
| `NAME_CONTRACT_TYPE` | 2 levels as-is | Mild driver (cash 8.3% / revolving 5.5%). |
| `AGE_YEARS` (`-DAYS_BIRTH/365.25`) | **Fixed domain bands** (5-yr) | Strong monotonic driver. Count-check the thin 65–69 band. |
| `EMP_YEARS` (`-DAYS_EMPLOYED/365.25`) | Fixed milestone bands + **sentinel/missing as own bin** | Sentinel group is mostly low-risk pensioners. Count-check 20+ band. |
| `NAME_INCOME_TYPE` | Pool sparse levels before WOE | Maternity/Unemployed = tiny high-risk; Student/Businessman = 0-default → **infinite WOE** if unpooled. Pool by *similar rate*. Disambiguates the DAYS_EMPLOYED sentinel. |
| `OCCUPATION_TYPE` | Pool <5% levels; keep NaN bin | ~31% missing. |
| `ORGANIZATION_TYPE` → `ORG_BAND` | Rate-banded → **refit on TRAIN in 5.1** | Currently built on full data = leakage. Recompute rate/bands on train only. |
| `NAME_EDUCATION_TYPE` | **Ordinal** WOE in education order | Clean gradient (Academic 1.8% → Lower secondary 10.9%). Expect monotonic WOE; merge sparse Academic level up. |
| `NAME_FAMILY_STATUS`, `NAME_HOUSING_TYPE` | Nominal WOE; pool sparse | Pool the 'Unknown' family-status singleton. |
| `CNT_CHILDREN` / `CNT_FAM_MEMBERS` | Cap tail to `5+`; **keep one** | Collinear (children ⊂ family members). Drop the redundant one at selection. |
| `CODE_GENDER` | **Exclude from model** | Protected attribute (responsible lending / anti-discrimination). EDA context only. Screen retained drivers for gender proxying. |
| `NAME_TYPE_SUITE` | Weak; candidate to drop | Narrow spread (7.4–9.8%). |
| §4 ratios (DTI, CREDIT_INCOME, ANNUITY_CREDIT, CREDIT_GOODS, EMPLOYED_AGE) | Quantile bins; EMPLOYED_AGE missing = own bin | The affordability signal the loan amounts lacked. |

---

## 3. Cross-cutting discipline rules (non-negotiable for a clean screen)

1. **Split first, fit on train only.** The 80/20 stratified split (cell 160) must precede *all* supervised steps. Every bin edge, every WOE map, every rate-band (ORG_BAND) is **fit on train and applied to validation** — never refit on val. This is the leakage rule; it's the single thing most likely to inflate your IV table if broken.
2. **Empty / tiny bins.** Guard WOE against zero-bad bins (epsilon or merge — your helper uses `1e-6`; prefer *merging* sparse bins where possible and say which). Enforce a **minimum count of both goods and bads per bin**.
3. **Missing as its own bin** wherever missingness is informative (EXT scores, EMPLOYED_AGE/sentinel).
4. **Gender excluded**, and its proxies checked.
5. **IV bands (Siddiqi):** <0.02 drop · 0.02–0.1 weak · 0.1–0.3 medium · 0.3–0.5 strong · **>0.5 → suspect leakage/artefact, investigate before celebrating**.
6. **Read every bin default rate against the ~8.1% base rate.**

---

## 4. Open fixes / re-runs before continuing

- **Re-run the edited cells** so outputs match the corrected code: statistical-typing cell (SK_ID_CURR → `id`), ranked-missingness & building-stats charts (label fixes), the new **Score Intercorrelation** cell (no output yet), the EXT overlay (new palette).
- **Numbering bug:** two `### 4.3` headers exist — `Outlier Skew-Treatment` and `Missing-Values Handling`. Renumber the second to **4.4**.
- **ORG_BAND leakage:** relocate/recompute in 5.1 on train (see §2).
- **WOE helper gap (important):** `calc_woe_iv` calls `pd.qcut` *inside* the function, so it re-derives bin edges from whatever frame it's given. For train/val discipline you need to **fit edges on train and apply the same edges to val** (`pd.qcut(train, retbins=True)` → `pd.cut(val, bins=edges)`), otherwise val is silently re-binned on its own quantiles. Add a fit/apply split to the helper (or a thin wrapper) before 5.3.

---

## 5. Step-by-step remaining work

### 3.5 Other Numericals (light touch)
Families: `client_timeline` (DAYS_REGISTRATION/ID_PUBLISH/LAST_PHONE_CHANGE), `social_circle` (OBS/DEF_30/60_CNT), `bureau_enquiries` (AMT_REQ_*). For each: quick shape check, confirm the block-wise missingness from 2.3, default-rate-by-bin. Expectation from 2.3: these are likely **weak** — DEF_*_CNT_SOCIAL_CIRCLE (counts of the applicant's social circle who defaulted) may carry modest signal; most others low. Decision per feature: keep-and-bin or drop. Fill Observation cells [141]/[143].

### §4 Feature Engineering
- **4.1** ratios already coded (cell 148) — five ratios with `_safe_div`. Run `.describe()`, fill Observation [149] with ranges/tails. These map directly to the affordability signal predicted in the 3.2 walkthrough (DTI≈serviceability/NSR, CREDIT_INCOME≈leverage, CREDIT_GOODS≈LVR).
- **4.2** default-rate-by-bin per ratio (cell 152) — confirm each shows a cleaner gradient than the raw amounts did. Fill Observation [153].
- **4.3 Outlier/Skew** — ratios can have extreme values (div by tiny income). Cap/winsorise or trust quantile binning (rank-based → robust). Decide and document.
- **4.4 Missing-Values Handling** — state per-feature treatment (missing-as-bin vs drop). No imputation needed for a screen.

### §5 WOE/IV
- **5.1** split done (cell 160). Assemble the binned-feature frame **from the §2 table above**, fit on train. Refit ORG_BAND here.
- **5.2** `calc_woe_iv` done (cell 163) — add the fit/apply-edges fix from §4.
- **5.3** loop all binned features → ranked IV table (sorted desc, band-labelled).
- **5.4** top-10 drivers styled table (feeds the deck). Expect EXT scores + ratios + age/education near the top.
- **5.5** WOE encoding — apply train-fit WOE maps to train/val (cell 172 pseudocode is the pattern). These WOE frames are the modelling input.
- **5.6** optbinning cross-check (optional) — `OptimalBinning` for monotonic bins on the top numeric drivers; compare IV to your manual version.

### Feature selection (close of screening)
- Drop IV < 0.02; flag IV > 0.5 for leakage.
- Drop redundant/collinear pairs (CNT_CHILDREN vs CNT_FAM_MEMBERS; EXT scores if intercorrelation is high; AMT_CREDIT vs AMT_GOODS_PRICE are ~identical).
- Confirm gender excluded + no strong proxies.
- Output: the defensible shortlist that would go into the scorecard.

### §6–8
- **6 Findings** — the ranked IV table + written interpretation of top drivers (why each makes credit sense; flag any artefact).
- **7 Next Steps** — checkable actions carried into modelling.
- **8 Assumptions/Limitations/Lineage** — state the `TARGET` definition (payment-difficulty proxy, not full default), the application-time-only scope (6 behavioural tables not used), the sentinel/missing treatments, the train/val split + seed, gender exclusion.

---

## 6. Deliverables to finish the project (from the brief)
- [ ] Notebook runs top-to-bottom, reproducible, no stale outputs.
- [ ] Ranked IV table (every screened feature, sorted, band-labelled).
- [ ] **Quarto reveal.js deck** for a non-technical audience: answer first, IV explained in one line, ranked-drivers bar chart, one default-rate-by-band chart, a caveats slide (missingness, gender exclusion, leakage checks), a recommendation.

---

## 7. Transition to modelling (Project 3)
- Modelling input = the **WOE-encoded train/val frames** + the stored `{bin → WOE}` maps (needed to score new applicants).
- First model = **logistic-regression scorecard** on the WOE features (WOE encoding makes LR coefficients directly interpretable as points).
- Carry over: the feature shortlist, the binning maps, the train/val split + seed, and the gender-exclusion / proxy notes. Validate with the same discrimination metrics you learned here (Gini/KS) on the held-out val set.

---

_Golden rule for the rest of the build: **split first, fit on train, apply to val.** If an IV looks too good, suspect leakage before celebrating._
