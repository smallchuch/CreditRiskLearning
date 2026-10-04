# CR01 - Portfolio snapshot and concentration

`answers/cr01_portfolio_concentration/qNN.sql` &nbsp;|&nbsp; check with: `grade cr01` or `grade cr01 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Scenario: you've just joined the credit risk analytics team

Your manager says: *"Before anything else, tell me what the book looks like."* This set is the first-week portfolio snapshot every analyst builds.

**Definitions used throughout the credit-risk sets** (write them in your own notes):
* **The live book at 2025-12-31** = rows of `loan_monthly_snapshot` where `snapshot_date = '2025-12-31'` and `loan_status <> 'Closed'`.
* **Exposure / balance** = `closing_balance`.
* **LVR (origination)** = `loan.lvr_at_origination_pct`; current LVR is in `ecl_provision_quarterly.current_lvr_pct`.
* **Concentration** = how much of the book sits in one bucket (state, product, broker, high-LVR...). Regulators and boards watch these.

```
   Live book  -->  slice by:  state | product | purpose | channel | LVR band | repayment type | broker
                   measure:   count | balance | share of total | average rate | weighted LVR
```
Weighted averages: `SUM(x * balance) / SUM(balance)`. Simple averages treat a $50k loan like a $2m loan - committees want the weighted view.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Headline numbers: loans in the live book, total balance (0dp) and average balance (0dp). One row: `loans`, `total_balance`, `avg_balance`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Balance by loan `purpose` with share of book (1dp %). Return `purpose`, `balance` (0dp), `share_pct`; sorted by balance descending.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Investor vs owner-occupier: using `dim_product.occupancy`, balance (0dp) and share (1dp) by occupancy. Return `occupancy`, `balance`, `share_pct`; sorted by occupancy.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

Geographic concentration: balance share (1dp) by `dim_postcode.state` of the security property. `state`, `balance` (0dp), `share_pct`; sorted by balance descending.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

Interest-only share of the live book: % of balance on `repayment_type = 'Interest Only'` at 2025-12-31 (2dp). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q06 &nbsp; ★★ &nbsp; (core)

Balance-weighted average interest rate (3dp) by `rate_type` of the loan. Return `rate_type`, `wtd_rate`; sorted by `rate_type`. Use snapshot `interest_rate_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

Channel mix of the live book by balance (1dp %). `channel`, `share_pct`; sorted by share descending.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

Broker concentration: top 10 brokers by live balance and their share of the whole book (2dp). Return `broker_id`, `balance` (0dp), `share_pct`; sorted by balance descending.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

Large exposures: number of live loans with balance over $1.5m and their combined balance (0dp). Two numbers: `loans`, `balance`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q10 &nbsp; ★★★ &nbsp; (challenge)

Customer-level concentration: top 10 primary customers by total live balance across all their loans. `primary_customer_id`, `loans`, `total_balance` (0dp); sorted by balance descending, id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

High-LVR book at origination: share of live balance with `lvr_at_origination_pct > 80` (2dp), and with `> 90` (2dp). Return `pct_gt80`, `pct_gt90`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Product x state: for each property state, the product (`product_name`) with the largest live balance. Return `state`, `product_name`, `balance` (0dp); sorted by state.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

Herfindahl-Hirschman index (HHI) of state concentration: sum over states of (share of book)^2 where share is a fraction (e.g. 0.25), times 10,000, rounded to 0dp. One number: `hhi`.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

Portfolio growth: live balance at each year-end 2019-2025 and the growth vs prior year-end (%, 1dp). Return `year_end` (date), `balance` (0dp), `growth_pct`; sorted by date.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★★ &nbsp; (challenge)

Average loan size by origination year for live loans (balance at 2025-12-31 and original amount both, 0dp). Return `yr`, `avg_original`, `avg_balance`; sorted by yr.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★ &nbsp; (core)

Property state `'NSW'` at 2025-12-31: live loans, total balance (0 dp), share of the whole book (2 dp %) and balance-weighted interest rate (3 dp). `loans`, `balance`, `share_pct`, `wtd_rate`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★★ &nbsp; (core)

Property state `'VIC'` at 2025-12-31: live loans, total balance (0 dp), share of the whole book (2 dp %) and balance-weighted interest rate (3 dp). `loans`, `balance`, `share_pct`, `wtd_rate`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★ &nbsp; (core)

Property state `'QLD'` at 2025-12-31: live loans, total balance (0 dp), share of the whole book (2 dp %) and balance-weighted interest rate (3 dp). `loans`, `balance`, `share_pct`, `wtd_rate`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★★ &nbsp; (core)

Property state `'SA'` at 2025-12-31: live loans, total balance (0 dp), share of the whole book (2 dp %) and balance-weighted interest rate (3 dp). `loans`, `balance`, `share_pct`, `wtd_rate`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★★ &nbsp; (core)

Property state `'WA'` at 2025-12-31: live loans, total balance (0 dp), share of the whole book (2 dp %) and balance-weighted interest rate (3 dp). `loans`, `balance`, `share_pct`, `wtd_rate`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★ &nbsp; (core)

Property state `'TAS'` at 2025-12-31: live loans, total balance (0 dp), share of the whole book (2 dp %) and balance-weighted interest rate (3 dp). `loans`, `balance`, `share_pct`, `wtd_rate`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★ &nbsp; (core)

Property state `'NT'` at 2025-12-31: live loans, total balance (0 dp), share of the whole book (2 dp %) and balance-weighted interest rate (3 dp). `loans`, `balance`, `share_pct`, `wtd_rate`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★ &nbsp; (core)

Property state `'ACT'` at 2025-12-31: live loans, total balance (0 dp), share of the whole book (2 dp %) and balance-weighted interest rate (3 dp). `loans`, `balance`, `share_pct`, `wtd_rate`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★★ &nbsp; (core)

Purpose `'Purchase - Owner Occupied'` live book at 2025-12-31: loans, balance (0 dp), average origination LVR (1 dp), weighted rate (3 dp). `loans`, `balance`, `avg_lvr`, `wtd_rate`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★★ &nbsp; (core)

Purpose `'Purchase - Investment'` live book at 2025-12-31: loans, balance (0 dp), average origination LVR (1 dp), weighted rate (3 dp). `loans`, `balance`, `avg_lvr`, `wtd_rate`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★★ &nbsp; (core)

Purpose `'Refinance'` live book at 2025-12-31: loans, balance (0 dp), average origination LVR (1 dp), weighted rate (3 dp). `loans`, `balance`, `avg_lvr`, `wtd_rate`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★★ &nbsp; (core)

Purpose `'Equity Release / Top-up'` live book at 2025-12-31: loans, balance (0 dp), average origination LVR (1 dp), weighted rate (3 dp). `loans`, `balance`, `avg_lvr`, `wtd_rate`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★★ &nbsp; (core)

Purpose `'Construction'` live book at 2025-12-31: loans, balance (0 dp), average origination LVR (1 dp), weighted rate (3 dp). `loans`, `balance`, `avg_lvr`, `wtd_rate`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★★ &nbsp; (core)

Purpose `'Internal Refinance'` live book at 2025-12-31: loans, balance (0 dp), average origination LVR (1 dp), weighted rate (3 dp). `loans`, `balance`, `avg_lvr`, `wtd_rate`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★★ &nbsp; (core)

Channel `'Broker'` live book: balance (0 dp) split by product occupancy. `occupancy`, `balance`, `share_pct` (share within the channel, 1 dp); sorted by occupancy.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q31 &nbsp; ★★ &nbsp; (core)

Channel `'Branch'` live book: balance (0 dp) split by product occupancy. `occupancy`, `balance`, `share_pct` (share within the channel, 1 dp); sorted by occupancy.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q32 &nbsp; ★★ &nbsp; (core)

Channel `'Digital'` live book: balance (0 dp) split by product occupancy. `occupancy`, `balance`, `share_pct` (share within the channel, 1 dp); sorted by occupancy.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q33 &nbsp; ★★ &nbsp; (core)

Channel `'Mobile Lender'` live book: balance (0 dp) split by product occupancy. `occupancy`, `balance`, `share_pct` (share within the channel, 1 dp); sorted by occupancy.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★ &nbsp; (warm-up)

Book size at 2019-12-31: live loans, total balance (0 dp), average balance (0 dp), largest balance (0 dp). `loans`, `balance`, `avg_balance`, `max_balance`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q35 &nbsp; ★ &nbsp; (warm-up)

Book size at 2020-12-31: live loans, total balance (0 dp), average balance (0 dp), largest balance (0 dp). `loans`, `balance`, `avg_balance`, `max_balance`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q36 &nbsp; ★ &nbsp; (warm-up)

Book size at 2021-12-31: live loans, total balance (0 dp), average balance (0 dp), largest balance (0 dp). `loans`, `balance`, `avg_balance`, `max_balance`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q37 &nbsp; ★ &nbsp; (warm-up)

Book size at 2022-12-31: live loans, total balance (0 dp), average balance (0 dp), largest balance (0 dp). `loans`, `balance`, `avg_balance`, `max_balance`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q38 &nbsp; ★ &nbsp; (warm-up)

Book size at 2023-12-31: live loans, total balance (0 dp), average balance (0 dp), largest balance (0 dp). `loans`, `balance`, `avg_balance`, `max_balance`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q39 &nbsp; ★ &nbsp; (warm-up)

Book size at 2024-12-31: live loans, total balance (0 dp), average balance (0 dp), largest balance (0 dp). `loans`, `balance`, `avg_balance`, `max_balance`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q40 &nbsp; ★ &nbsp; (warm-up)

Book size at 2025-12-31: live loans, total balance (0 dp), average balance (0 dp), largest balance (0 dp). `loans`, `balance`, `avg_balance`, `max_balance`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q41 &nbsp; ★★★ &nbsp; (challenge)

Top-5 concentration: the share of the live balance (2 dp %) held by the largest 5 primary customers (by total balance across their loans). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q42 &nbsp; ★★★ &nbsp; (challenge)

Top-10 concentration: the share of the live balance (2 dp %) held by the largest 10 primary customers (by total balance across their loans). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q43 &nbsp; ★★★ &nbsp; (challenge)

Top-20 concentration: the share of the live balance (2 dp %) held by the largest 20 primary customers (by total balance across their loans). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.
