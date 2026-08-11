# Research Foundation — Modelling NG / CGT / Stamp Duty Counterfactuals on Australian State Housing Markets

*Compiled August 2026. A living reference for a counterfactual (back-dated, grandfathering-preserved) study of the 2026 federal tax changes and a state stamp-duty scenario. Expand as the project develops.*

**The three levers being modelled**
1. Negative gearing quarantined to new builds (net rental losses on established dwellings no longer deductible against non-rental income) — enacted 12 May 2026, grandfathered.
2. CGT 50% discount replaced by cost-base indexation + 30% minimum tax on net gains — from 1 July 2027, new builds can elect to keep the discount.
3. A capped stamp-duty scenario (your own construct — no single enacted federal event; state-based).

Replay design: **with grandfathering preserved**, so effects build gradually as the stock turns over, and the headline output is the **established-vs-new price divergence** and induced construction, not a single price number.

---

## 1. Australian Housing Supply & Sale-Price Data

### Transaction prices (the "ground truth" — actual sales)

| Source | What it covers | Granularity | Access | Notes |
|---|---|---|---|---|
| **State Valuers-General / Land Registries** (e.g. [VG Victoria property sales statistics](https://www.land.vic.gov.au/valuations/resources-and-reports/property-sales-statistics), NSW Valuer General / NSW LRS bulk sales, QLD, SA Landata, WA Landgate) | Every completed property transfer (price, address, property type, land area) | Unit-record, address level | Some free aggregates; unit-record via paid bulk data or DataLab | **This is the primary feed** most commercial indices are built on. Best for repeat-sales and spatial work. |
| **CoreLogic / Cotality** (RP Data) | Daily Home Value Index (hedonic), sales, valuations, rents | Suburb → dwelling | Commercial (paid) | Industry-standard indices; hedonic method. Renamed Cotality 2025. |
| **PropTrack** (REA Group) | [Home Price Index](https://www.proptrack.com.au/), listings | Suburb → dwelling | Commercial; some free reports | Built from VG data + realestate.com.au listings. |
| **Domain** | House Price Report, listings, rents | Capital city / region | Free reports; data commercial | Median-based; differs from hedonic sources. |
| **SQM Research** | Asking prices, stock-on-market, rental vacancy rates | Postcode → capital city | Some free, some paid | Good for *listing/asking* vs *sold* gap and inventory. |

> **Caveat to bake in:** ABS, CoreLogic, PropTrack, Domain and SQM "rarely agree" on price movements in any given market because of method (median vs hedonic vs stratified) and timing (settlement vs contract vs listing). Pick one method per model and document it.

### Official price & supply series (ABS)

- **[Total Value of Dwellings](https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/total-value-dwellings/latest-release)** (quarterly) — total dwelling stock value, **median price and number of residential transfers by state**. *Note: the old Residential Property Price Index (cat. 6416.0) was discontinued after Dec quarter 2021; this series replaced it.*
- **[Building Approvals, Australia](https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/latest-release)** (cat. 8731.0, monthly) — dwelling approvals by type (house vs units), by state and SA2/LGA. **Core supply-side leading indicator.**
- **Building Activity, Australia** (cat. 8752.0, quarterly) — commencements, completions, work done, dwellings under construction. The realised-supply counterpart to approvals.
- **Census of Population and Housing** (2021; next 2026) — dwelling counts, tenure, occupancy, dwelling structure at mesh-block level. Foundational for dwelling stock.
- **Regional population / dwelling estimates** — for denominators and per-capita supply.

### Government & institutional portals

- **[housingdata.gov.au](https://www.housingdata.gov.au/)** — National Housing Supply and Affordability Council portal; visualisations incl. "Australian property sales by value," supply pipeline, affordability.
- **Housing Australia (formerly NHFIC)** — *State of the Nation's Housing* reports; supply/demand projections to 2030s.
- **RBA statistical tables** — housing prices and related series in the [statistical tables](https://www.rba.gov.au/statistics/tables/); underpins the RBA housing model.
- **AIHW** — housing assistance and social-housing data (supply of subsidised stock).

---

## 2. Income, Wealth, Cash & Borrowing-Power Data

### Household income & wealth (levels and distribution)

- **ABS Survey of Income and Housing (SIH)** — household income, **net worth**, housing costs, tenure; conducted in current form since 2003–04 (wealth every cycle since 2003–04 except 2007–08). Microdata via **ABS TableBuilder / DataLab**. The workhorse for distributional / purchasing-power analysis.
- **ABS Household Income and Wealth, Australia** (cat. 6523.0) — published SIH outputs.
- **HILDA Survey** (Melbourne Institute) — **longitudinal panel since 2001**, annual: income, wealth, housing, tenure transitions, attitudes. Restricted-release microdata. Best for *dynamics* (who becomes an investor, mobility, lock-in). Latest: [20th Annual Statistical Report](https://melbourneinstitute.unimelb.edu.au/hilda).
- **ABS National Accounts — household balance sheet** — aggregate housing assets, mortgage liabilities, net worth over time.

### Tax data (directly measures negative gearing intensity)

- **ATO Taxation Statistics** — individual and **postcode-level** taxable income, **and critically: number of individuals claiming rental interest deductions, aggregate net rental income/loss, and rental property counts**. This is the single most direct measure of *negative-gearing intensity by geography and income band*, plus CGT event data. Reports mean (not median) income by postcode. **Use this to calibrate the size of the treated population.**

### Wages & earnings

- **ABS Wage Price Index** (cat. 6345.0) and **Average Weekly Earnings** (cat. 6302.0) — income growth for affordability/serviceability denominators.

### Credit, lending & borrowing power

- **ABS Lending Indicators** (cat. 5601.0, monthly) — **new housing loan commitments split by owner-occupier vs investor**, by state. Key for the investor-share time series.
- **APRA** — [Quarterly ADI Property Exposures](https://www.apra.gov.au/quarterly-authorised-deposit-taking-institution-statistics) and monthly ADI statistics (loan flows, LVR/DTI/interest-only shares); **serviceability buffer settings** (3.0pp since Oct 2021) — a ~50bp buffer change ≈ ~5% change in max borrowing capacity, so this is a direct borrowing-power lever to hold constant or vary.
- **RBA statistical tables** — credit aggregates (D tables), lending rates (F tables), household debt-to-income and debt-servicing ratios (E tables).
- **Census** — household income, mortgage/rent payments, tenure at fine geography for spatial affordability.

> **Modelling tip:** borrowing power ≈ f(income, interest rate, serviceability buffer, existing debt, deposit/wealth). The ATO rental-deduction data + SIH wealth + Lending Indicators investor share together let you separate *investor* purchasing power from *owner-occupier* — essential when the whole point is a tax change that hits only investors on established stock.

---

## 3. Studies on These Specific Policies

### Negative gearing & CGT discount (Australia)

- **RBA — Saunders & Tulip, *A Model of the Australian Housing Market*** (RDP 2019-01) — the reference structural model for price/supply; good scaffolding for your capitalisation elasticity. Plus the **[RBA submission to the Inquiry into Home Ownership](https://www.rba.gov.au/publications/submissions/housing-and-housing-finance/inquiry-into-home-ownership/impact-of-taxation.html)** on the impact of taxation (explains the 1999 CGT switch to nominal-half-rate and its effect on asset attractiveness).
- **RBA — Kendall & Tulip, *The Effect of Zoning on Housing Prices*** (RDP 2018-03) — supply-constraint magnitude; useful for the supply side of the counterfactual.
- **Grattan Institute** — *Hot Property* (2016) and ongoing work; recent **[Reforming the Capital Gains Tax discount](https://grattan.edu.au/wp-content/uploads/2026/03/HES_2025_CGTSub.pdf)** (2025/26). Estimates: halving CGT discount + curbing NG ≈ prices ~1–2% lower; CGT reform alone ≈ ~10,000 fewer new homes to 2030 and <$1/week rent effect. Good for benchmarking your outputs' plausibility.
- **UTS (Journal of Housing and the Built Environment, 2023)** — [SVAR of negative gearing and investor decisions, Greater Sydney 1991–2018](https://link.springer.com/article/10.1007/s10901-023-10069-3). The closest existing method to what you're building; investors *increased* as yields fell.
- **ANU Centre for Social Research & Methods (Ben Phillips)** — [distributional modelling of NG and CGT](https://csrm.cass.anu.edu.au/research/publications/distributional-modelling-negative-gearing-and-capital-gains). Estimated ~1.5% price effect; strong on who benefits by income decile.
- **ACOSS — *Fuel on the Fire*** (2016) — [NG + CGT distributional case](https://www.acoss.org.au/wp-content/uploads/2016/04/Fuel_on_the_fire_ACOSS.pdf).
- **Parliamentary Budget Office** — costings of NG/CGT changes and [tax-mix efficiency explainers](https://www.pbo.gov.au/about-budgets/budget-insights/budget-explainers/tax-mix).
- **Henry Tax Review** (*Australia's Future Tax System*, 2010) — foundational framing of housing tax concessions.
- **Fane & Richardson**, *Capital gains, negative gearing and effective tax rates on income from rented houses* (ANU, 2004) — [effective-tax-rate mechanics](https://ideas.repec.org/p/pas/papers/2004-06.html).

### Stamp duty

- **Treasury — Cao et al., *Understanding the economy-wide efficiency and incidence of major Australian taxes*** (TWP 2015-01) — [excess-burden estimates](https://treasury.gov.au/sites/default/files/2019-03/TWP2015-01.pdf); stamp duty among the least efficient taxes.
- **Melbourne Institute WP 2021n08 — *Stamp duty and equity in Australia*** — [incidence & equity](https://melbourneinstitute.unimelb.edu.au/__data/assets/pdf_file/0004/3827344/wp2021n08.pdf).
- **Stamp duty and spatial misallocation** (Macroeconomic Dynamics, Cambridge, 2025) — welfare gains from cutting stamp duty ~3.6%, ~95% via the productivity/mobility channel. Directly relevant to a stamp-duty cap scenario.
- **Housing Australia (2021) — *Stamp Duty Reform: Benefits and Challenges*** — [reform analysis](https://www.housingaustralia.gov.au/sites/default/files/2022-10/stamp-duty-reform-benefits-challenges.pdf).
- **NSW Review / Productivity Commission** — stamp-duty-to-land-tax transition analysis; ACT's live 20-year transition is a real-world case study.

### Off-the-shelf turnover elasticities for the stamp-duty lever (international, cleanly identified)

- **Best & Kleven** — UK Stamp Duty Land Tax notches; transaction-volume elasticity.
- **Kopczuk & Munroe** — the NY/NJ "mansion tax" notch; bunching and turnover response.

---

## 4. International Evidence — Housing Price Dynamics & Investor Demand

### Direct analogues to negative-gearing quarantining (natural experiments)

- **New Zealand — removal of mortgage interest deductibility for residential investors (27 March 2021), phased out to 31 March 2025, then fully reversed 1 April 2025.** This is the **closest real-world analogue** to NG quarantining and it has a clean on/off/on structure — a natural experiment. Note IRD advised the change was unlikely to improve affordability, and the price slowdown coincided with rate rises, so *identification is contested* — a cautionary tale for your own attribution. ([The Conversation overview](https://theconversation.com/yes-nz-landlords-gain-from-the-repeal-of-interest-deductibility-rules-but-it-was-a-flawed-law-from-the-outset-218818)). NZ's **bright-line test** changes are a parallel CGT-proxy experiment.
- **UK — Section 24** (mortgage interest relief for buy-to-let restricted to basic-rate credit, phased 2017–2020). The other clean NG analogue; a large literature on landlord behaviour and rents.

### Institutional / investor concentration and prices (US)

- **Coven, *The Impact of Institutional Investors on Homeownership and Neighborhood Access*** ([JMP](https://joshuacoven.github.io/assets/JoshuaCovenJMP.pdf)).
- **Garriga, Gete & Tsouderou, *Investors and Housing Affordability*** — investor concentration ≈ +1.46pp price growth; robust to excluding superstar cities.
- **Autor, Palmer & Pathak (JPE 2014)** — [end of Cambridge rent control](https://economics.mit.edu/sites/default/files/publications/housing%20market%202014.pdf); large price spillovers to never-controlled units — a clean spillover-identification template.
- **Local Housing Solutions** — [evidence review on large-investor SFH purchases](https://www.localhousingsolutions.org/lab/notes/large-investors-single-family-homes/).

### Foreign capital / demand-shock natural experiments

- **Gorback & Keys, *Global Capital and Local Assets*** ([NBER 27370](https://www.nber.org/system/files/working_papers/w27370/w27370.pdf)) — +1% instrumented foreign capital ≈ +0.27% zip-code prices, tiny supply response; foreign-buyer-tax and Chinese-demand natural experiments (+8pp in high-exposure zips post-2011).
- **Badarinza & Ramadorai, *Home away from home?*** — foreign "safe-haven" demand and London prices.
- **Sá / JoEG** — [foreign investors and UK local house prices](https://academic.oup.com/joeg/advance-article/doi/10.1093/jeg/lbae043/7901283).
- **Foreign-buyer taxes** — Canada (BC 2016, Ontario NRST 2017), NZ foreign-buyer ban (2018) — a menu of demand-side policy shocks with quasi-experimental designs.
- **BIS CGFS Report 64 — *Property price dynamics: domestic and international drivers*** ([PDF](https://www.bis.org/publ/cgfs64.pdf)) — cross-country synthesis; good for framing.

### Supply elasticity (needed to close any counterfactual)

- **Hilber & Vermeulen** — UK planning constraints and house prices; the standard reference on how supply elasticity governs how much a demand shock capitalises into price vs quantity. Directly relevant to why grandfathering + new-build carve-outs make the *established-vs-new* split the key output.

---

## Method note — how these feed the model

- **Treatment population size** → ATO rental-deduction stats (who loses NG deductibility, by geography/income) + Lending Indicators investor share.
- **User-cost shock (NG + CGT)** → after-tax holding cost & required yield; calibrate capitalisation elasticity from RBA Saunders–Tulip and benchmark magnitude against Grattan/ANU.
- **Transaction-cost shock (stamp duty)** → turnover elasticity from Best–Kleven / Kopczuk–Munroe; welfare/mobility from the Cambridge spatial-misallocation paper.
- **Counterfactual engine** → synthetic control on state price series (VG/Cotality), with grandfathering replayed so the treated stock phases in; supply response bounded by a supply-elasticity assumption (Hilber–Vermeulen / Kendall–Tulip).
- **Headline outputs** → established-vs-new price divergence, investor-share path, induced dwelling approvals — not a single "prices X% lower" figure.
- **Honesty check** → the NZ case shows how easily a rate cycle confounds a tax-change attribution; pre-register the identification and show the sensitivity fan.
