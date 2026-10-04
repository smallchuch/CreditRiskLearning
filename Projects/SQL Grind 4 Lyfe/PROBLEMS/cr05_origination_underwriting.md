# CR05 - Origination funnel, serviceability and underwriting

`answers/cr05_origination_underwriting/qNN.sql` &nbsp;|&nbsp; check with: `grade cr05` or `grade cr05 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Scenario: origination funnel and underwriting quality

Applications flow through **lodged -> assessed -> decided -> settled**. The credit team asks: where do we lose people, why do we decline them, and are we approving risky ones?

```
 Lodged  ->  Decided  ->  Approved  ->  Settled
  100%        ~85%         ~60%          ~55%      <- typical funnel shape
```

Key columns: `loan_application` (status, decision, decline reason, exception flag), `application_assessment` (the serviceability workings):
* **NSR** (net serviceability ratio) = assessed net income / assessed commitments. Policy minimum lives in `ref_serviceability_policy.min_nsr`.
* **DTI** = total debt after settlement / gross income (`dti_ratio`).
* **HEM** = household expenditure measure (benchmark living costs); `hem_applied_flag` = benchmark used instead of declared expenses.
* `buffer_pct`: serviceability buffer added to the rate (2.5-3%) per policy epoch.
* **Policy exception** = approved despite breaching a rule (`policy_exception_flag`, `policy_exception_reason`).

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Funnel counts for 2025: applications lodged in 2025, how many decided (decision not null), approved, settled (`current_status='Settled'`). One row: `lodged`, `decided`, `approved`, `settled`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Decline reasons (with description) for 2025 declines: `reason_description`, `declines`; sorted by declines descending then description.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Average assessed NSR and DTI (2dp each) across all application assessments. Two numbers: `avg_nsr`, `avg_dti`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q04 &nbsp; ★★ &nbsp; (core)

Approval rate by year (decided apps only, 1dp): `yr`, `approval_pct`; sorted by year (application year).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

Serviceability declines by policy epoch: for applications declined with code 'SERV', the count per `policy_id` (range join application_date to policy). `policy_id`, `serv_declines`; sorted by policy.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

Approved applications where the assessed NSR is below the policy minimum (`ref_serviceability_policy.min_nsr` for the epoch of the application) - i.e. approved below the minimum. Count them. One number (policy exceptions may explain them).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q07 &nbsp; ★★ &nbsp; (core)

Of those below-minimum approvals, how many carry a `policy_exception_flag`? Return `below_min_approved`, `with_exception`, `without_exception`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q08 &nbsp; ★★ &nbsp; (core)

HEM usage: % of assessments where the HEM benchmark was applied (`hem_applied_flag`), by application year (1dp). `yr`, `hem_pct`; sorted by year.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

High DTI lending: approved applications with `dti_ratio >= 6`: counts by year of application. `yr`, `high_dti_approvals`; sorted by year.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★ &nbsp; (core)

Time-to-decision by channel (median days, 1dp) for decided applications. `channel`, `median_days`; sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Assessor outcomes: for assessors with at least 500 decided applications, the approval rate (1dp) and exception rate among approvals (1dp). `assessor_staff_id`, `decided`, `approval_pct`, `exception_pct`; sorted by `decided` descending then id. Top 10 rows.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Resizing: for applications that became loans, the share where the loan `original_amount` is below `requested_amount` (cut down by credit) - by channel (1dp %). `channel`, `resized_pct`; sorted by channel. Use a 1-dollar tolerance.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

Resubmission funnel: of applications that were declined, how many were followed by a resubmission (some later application has `resubmission_of_application_id` = this one), and how many of those resubmissions were approved? `declined`, `resubmitted`, `resubmitted_approved`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

Income verification: for approved applications in 2025, the % whose total `declared_annual_amount` differs from total verified (verified NULL treated as the declared value) by more than 5% - overstated income. One number (2dp). Aggregate income per application first.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q15 &nbsp; ★★★ &nbsp; (challenge)

Broker accreditation compliance: applications lodged via a broker where the application_date is BEFORE the broker's `accreditation_date` (should be 0). Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q16 &nbsp; ★ &nbsp; (warm-up)

Funnel for applications lodged in 2019: lodged, decided, approved, settled and the settle rate of lodged (1 dp %). `lodged`, `decided`, `approved`, `settled`, `settle_pct`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★ &nbsp; (warm-up)

Funnel for applications lodged in 2020: lodged, decided, approved, settled and the settle rate of lodged (1 dp %). `lodged`, `decided`, `approved`, `settled`, `settle_pct`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★ &nbsp; (warm-up)

Funnel for applications lodged in 2021: lodged, decided, approved, settled and the settle rate of lodged (1 dp %). `lodged`, `decided`, `approved`, `settled`, `settle_pct`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★ &nbsp; (warm-up)

Funnel for applications lodged in 2022: lodged, decided, approved, settled and the settle rate of lodged (1 dp %). `lodged`, `decided`, `approved`, `settled`, `settle_pct`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★ &nbsp; (warm-up)

Funnel for applications lodged in 2023: lodged, decided, approved, settled and the settle rate of lodged (1 dp %). `lodged`, `decided`, `approved`, `settled`, `settle_pct`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★ &nbsp; (warm-up)

Funnel for applications lodged in 2024: lodged, decided, approved, settled and the settle rate of lodged (1 dp %). `lodged`, `decided`, `approved`, `settled`, `settle_pct`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★ &nbsp; (warm-up)

Funnel for applications lodged in 2025: lodged, decided, approved, settled and the settle rate of lodged (1 dp %). `lodged`, `decided`, `approved`, `settled`, `settle_pct`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★ &nbsp; (core)

Decline reasons for `'Broker'` applications: `reason_description`, `declines`, `share_pct` (of the channel's declines, 1 dp); sorted by declines descending then description.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q24 &nbsp; ★★ &nbsp; (core)

Decline reasons for `'Branch'` applications: `reason_description`, `declines`, `share_pct` (of the channel's declines, 1 dp); sorted by declines descending then description.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q25 &nbsp; ★★ &nbsp; (core)

Decline reasons for `'Digital'` applications: `reason_description`, `declines`, `share_pct` (of the channel's declines, 1 dp); sorted by declines descending then description.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q26 &nbsp; ★★ &nbsp; (core)

Decline reasons for `'Mobile Lender'` applications: `reason_description`, `declines`, `share_pct` (of the channel's declines, 1 dp); sorted by declines descending then description.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q27 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2019 with assessments: average NSR (2 dp), average DTI (2 dp), % with HEM applied (1 dp). `avg_nsr`, `avg_dti`, `hem_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2020 with assessments: average NSR (2 dp), average DTI (2 dp), % with HEM applied (1 dp). `avg_nsr`, `avg_dti`, `hem_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2021 with assessments: average NSR (2 dp), average DTI (2 dp), % with HEM applied (1 dp). `avg_nsr`, `avg_dti`, `hem_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2022 with assessments: average NSR (2 dp), average DTI (2 dp), % with HEM applied (1 dp). `avg_nsr`, `avg_dti`, `hem_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q31 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2023 with assessments: average NSR (2 dp), average DTI (2 dp), % with HEM applied (1 dp). `avg_nsr`, `avg_dti`, `hem_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q32 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2024 with assessments: average NSR (2 dp), average DTI (2 dp), % with HEM applied (1 dp). `avg_nsr`, `avg_dti`, `hem_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q33 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2025 with assessments: average NSR (2 dp), average DTI (2 dp), % with HEM applied (1 dp). `avg_nsr`, `avg_dti`, `hem_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q34 &nbsp; ★★★ &nbsp; (challenge)

Policy exceptions in 2019: approved applications, those with a policy exception, the exception rate (2 dp %) and the most common exception reason. `approved`, `exceptions`, `exception_pct`, `top_reason`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q35 &nbsp; ★★★ &nbsp; (challenge)

Policy exceptions in 2020: approved applications, those with a policy exception, the exception rate (2 dp %) and the most common exception reason. `approved`, `exceptions`, `exception_pct`, `top_reason`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q36 &nbsp; ★★★ &nbsp; (challenge)

Policy exceptions in 2021: approved applications, those with a policy exception, the exception rate (2 dp %) and the most common exception reason. `approved`, `exceptions`, `exception_pct`, `top_reason`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q37 &nbsp; ★★★ &nbsp; (challenge)

Policy exceptions in 2022: approved applications, those with a policy exception, the exception rate (2 dp %) and the most common exception reason. `approved`, `exceptions`, `exception_pct`, `top_reason`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q38 &nbsp; ★★★ &nbsp; (challenge)

Policy exceptions in 2023: approved applications, those with a policy exception, the exception rate (2 dp %) and the most common exception reason. `approved`, `exceptions`, `exception_pct`, `top_reason`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q39 &nbsp; ★★★ &nbsp; (challenge)

Policy exceptions in 2024: approved applications, those with a policy exception, the exception rate (2 dp %) and the most common exception reason. `approved`, `exceptions`, `exception_pct`, `top_reason`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q40 &nbsp; ★★★ &nbsp; (challenge)

Policy exceptions in 2025: approved applications, those with a policy exception, the exception rate (2 dp %) and the most common exception reason. `approved`, `exceptions`, `exception_pct`, `top_reason`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q41 &nbsp; ★★★ &nbsp; (challenge)

`'Broker'` channel: approval rate (decided only, 1 dp %) for each year 2019-2025. `yr`, `approval_pct`; sorted by year.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q42 &nbsp; ★★★ &nbsp; (challenge)

`'Branch'` channel: approval rate (decided only, 1 dp %) for each year 2019-2025. `yr`, `approval_pct`; sorted by year.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q43 &nbsp; ★★★ &nbsp; (challenge)

`'Digital'` channel: approval rate (decided only, 1 dp %) for each year 2019-2025. `yr`, `approval_pct`; sorted by year.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q44 &nbsp; ★★★ &nbsp; (challenge)

`'Mobile Lender'` channel: approval rate (decided only, 1 dp %) for each year 2019-2025. `yr`, `approval_pct`; sorted by year.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.
