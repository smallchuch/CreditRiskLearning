# CR04 - Vintage and cohort credit performance

`answers/cr04_vintage_analysis/qNN.sql` &nbsp;|&nbsp; check with: `grade cr04` or `grade cr04 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Scenario: are newer loans performing worse than older ones?

**Vintage analysis** compares cohorts at the SAME AGE (months on book, MOB), not the same calendar date - so a 2023 loan at MOB 12 is compared with a 2021 loan at MOB 12.

```
   % 30+ DPD
     |        2023 vintage  /
     |      ------------ /  <- worse than 2021 at same age = tighter-than-it-should-have-been underwriting? or rate shock?
     |   2021 ........
     +-----------------------> months on book
```

Pattern:
```
 SELECT year(l.origination_date) AS vintage, s.months_on_book AS mob,
        COUNT(*) AS loans, COUNT(*) FILTER (WHERE s.days_past_due >= 30) AS bad
 FROM loan_monthly_snapshot s JOIN loan l USING (loan_id)
 GROUP BY 1, 2
```
Pay attention to the **denominator**: which loans are still observable at that MOB? Closed loans drop out (survivorship), and young vintages have no data for high MOBs.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Loans originated per year and their average original amount (0dp). `yr`, `loans`, `avg_amount`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Average origination LVR (1dp) and average interest rate (2dp) by origination year. `yr`, `avg_lvr`, `avg_rate`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★★ &nbsp; (core)

30+ DPD rate at MOB 6 (count basis, 2dp, non-closed) by origination year for 2019-2025. `yr`, `loans`, `pct_30plus`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

The vintage grid at MOB 3, 6, 12, 24 for origination years 2020-2023: 30+ DPD rate (2dp) laid out as columns. `yr`, `mob3`, `mob6`, `mob12`, `mob24`; sorted by year. Non-closed rows.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

Cumulative ever-90+ by origination year: % of each vintage's loans that have EVER been 90+ DPD (any snapshot, 2dp). `yr`, `loans`, `ever90_pct`; sorted by year. All loans in the vintage are the denominator.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

Attrition curve: % of the 2021 vintage (by loan count) still open at MOB 12, 24, 36, 48 (open = has a non-closed snapshot at that MOB), as % of loans originated in 2021. Return `mob`, `open_pct` (1dp); sorted by mob.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★★ &nbsp; (challenge)

Channel quality by vintage: for origination years 2021-2024, the ever-90+ rate (2dp) by channel as columns. `yr`, `broker`, `branch`, `digital`, `mobile`; sorted by year. Denominator = all loans of that vintage/channel.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Bureau score at origination vs later default: bucket the primary applicant's `bureau_score` at application (join via `loan.application_id` to `credit_bureau_report` for the primary customer) into `<600`, `600-699`, `700-799`, `800+`, with NULLs as `no score`; return the ever-90+ rate (2dp) per bucket. `score_band`, `loans`, `ever90_pct`; sorted by band label alphabetically.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★★ &nbsp; (challenge)

Policy-epoch performance: using the serviceability policy in force at the application date (`ref_serviceability_policy`), the ever-90+ rate (2dp) per `policy_id` for loans with an `application_id`. `policy_id`, `loans`, `ever90_pct`; sorted by policy_id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★★ &nbsp; (challenge)

Seasoning of arrears: at 2025-12-31, the 30+ DPD rate (count, 2dp) by months-on-book bucket `0-11`, `12-23`, `24-47`, `48+` for live loans. `mob_bucket`, `loans`, `rate_pct`; sorted by bucket's lower bound.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

First-year failures: loans that reached 30+ DPD within their first 6 months (MOB <= 6) - 'early payment defaults' - as a % of loans originated, by origination year (2019-2024, 2dp). `yr`, `loans`, `epd_pct`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★ &nbsp; (core)

The 2019 vintage by channel: loans and ever-90+ rate (2 dp %). `channel`, `loans`, `ever90_pct`; sorted by channel.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★ &nbsp; (core)

The 2020 vintage by channel: loans and ever-90+ rate (2 dp %). `channel`, `loans`, `ever90_pct`; sorted by channel.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q14 &nbsp; ★★ &nbsp; (core)

The 2021 vintage by channel: loans and ever-90+ rate (2 dp %). `channel`, `loans`, `ever90_pct`; sorted by channel.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★ &nbsp; (core)

The 2022 vintage by channel: loans and ever-90+ rate (2 dp %). `channel`, `loans`, `ever90_pct`; sorted by channel.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★ &nbsp; (core)

The 2023 vintage by channel: loans and ever-90+ rate (2 dp %). `channel`, `loans`, `ever90_pct`; sorted by channel.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q17 &nbsp; ★★ &nbsp; (core)

The 2024 vintage by channel: loans and ever-90+ rate (2 dp %). `channel`, `loans`, `ever90_pct`; sorted by channel.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q18 &nbsp; ★★ &nbsp; (core)

Purpose `'Purchase - Owner Occupied'`: 30+ DPD rate at MOB 12 (count, non-closed, 2 dp %) by origination year 2019-2024. `yr`, `loans`, `pct_30plus`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q19 &nbsp; ★★ &nbsp; (core)

Purpose `'Purchase - Investment'`: 30+ DPD rate at MOB 12 (count, non-closed, 2 dp %) by origination year 2019-2024. `yr`, `loans`, `pct_30plus`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q20 &nbsp; ★★ &nbsp; (core)

Purpose `'Refinance'`: 30+ DPD rate at MOB 12 (count, non-closed, 2 dp %) by origination year 2019-2024. `yr`, `loans`, `pct_30plus`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q21 &nbsp; ★★ &nbsp; (core)

Purpose `'Equity Release / Top-up'`: 30+ DPD rate at MOB 12 (count, non-closed, 2 dp %) by origination year 2019-2024. `yr`, `loans`, `pct_30plus`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q22 &nbsp; ★★ &nbsp; (core)

Purpose `'Construction'`: 30+ DPD rate at MOB 12 (count, non-closed, 2 dp %) by origination year 2019-2024. `yr`, `loans`, `pct_30plus`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q23 &nbsp; ★★★ &nbsp; (challenge)

Early payment default for `'Broker'`: % of loans reaching 30+ DPD within their first 6 months, by origination year 2019-2024 (2 dp %). `yr`, `loans`, `epd_pct`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q24 &nbsp; ★★★ &nbsp; (challenge)

Early payment default for `'Branch'`: % of loans reaching 30+ DPD within their first 6 months, by origination year 2019-2024 (2 dp %). `yr`, `loans`, `epd_pct`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q25 &nbsp; ★★★ &nbsp; (challenge)

Early payment default for `'Digital'`: % of loans reaching 30+ DPD within their first 6 months, by origination year 2019-2024 (2 dp %). `yr`, `loans`, `epd_pct`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q26 &nbsp; ★★★ &nbsp; (challenge)

Early payment default for `'Mobile Lender'`: % of loans reaching 30+ DPD within their first 6 months, by origination year 2019-2024 (2 dp %). `yr`, `loans`, `epd_pct`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q27 &nbsp; ★★★ &nbsp; (challenge)

Origination LVR above 0 and up to 70: the ever-90+ rate by origination year 2019-2024 (2 dp %). `yr`, `loans`, `ever90_pct`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q28 &nbsp; ★★★ &nbsp; (challenge)

Origination LVR above 70 and up to 80: the ever-90+ rate by origination year 2019-2024 (2 dp %). `yr`, `loans`, `ever90_pct`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q29 &nbsp; ★★★ &nbsp; (challenge)

Origination LVR above 80 and up to 90: the ever-90+ rate by origination year 2019-2024 (2 dp %). `yr`, `loans`, `ever90_pct`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q30 &nbsp; ★★★ &nbsp; (challenge)

Origination LVR above 90 and up to 200: the ever-90+ rate by origination year 2019-2024 (2 dp %). `yr`, `loans`, `ever90_pct`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.
