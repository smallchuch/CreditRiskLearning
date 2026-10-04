from ._gen import *
MORE_FOR = '14_data_quality'
PROBLEMS = []
KEYS = [("customer","customer_id"),("loan","loan_id"),("loan_application","application_id"),("property","property_id"),("dim_broker","broker_id"),("dim_staff","staff_id"),("dim_branch","branch_id"),
        ("credit_bureau_report","report_id"),("applicant_income","income_id"),("applicant_liability","liability_id"),("application_status_history","event_id"),("loan_event","event_id"),
        ("loan_rate_history","rate_history_id"),("loan_payment","payment_id"),("hardship_arrangement","hardship_id"),("collections_activity","activity_id"),("complaint","complaint_id"),("property_valuation","valuation_id"),("loan_security","security_id"),("dim_postcode","postcode")]
for t,k in KEYS:
    PROBLEMS.append(P(1, f"Key uniqueness test: how many values of `{k}` appear more than once in `{t}`? One number (0 = clean).",
      f"SELECT COUNT(*) FROM (SELECT {k} FROM {t} GROUP BY 1 HAVING COUNT(*)>1)"))
FKS = [("loan","product_id","dim_product","product_id"),("loan","primary_customer_id","customer","customer_id"),("loan","property_id","property","property_id"),("loan","assessor_staff_id","dim_staff","staff_id"),
       ("loan_application","primary_customer_id","customer","customer_id"),("loan_application","product_id","dim_product","product_id"),("loan_application","assessor_staff_id","dim_staff","staff_id"),
       ("loan_borrower","customer_id","customer","customer_id"),("loan_borrower","loan_id","loan","loan_id"),("application_applicant","customer_id","customer","customer_id"),
       ("credit_bureau_report","application_id","loan_application","application_id"),("applicant_income","application_id","loan_application","application_id"),("loan_security","property_id","property","property_id"),
       ("property","postcode","dim_postcode","postcode"),("complaint","customer_id","customer","customer_id"),("hardship_arrangement","loan_id","loan","loan_id"),("loan_event","loan_id","loan","loan_id"),("property_valuation","property_id","property","property_id")]
for ct,ck,pt,pk in FKS:
    PROBLEMS.append(P(2, f"Orphan check: rows in `{ct}` whose `{ck}` has no match in `{pt}.{pk}` (ignore NULL `{ck}`). Count. One number (0 = clean; if not 0, why?).",
      f"SELECT COUNT(*) FROM {ct} c WHERE c.{ck} IS NOT NULL AND NOT EXISTS (SELECT 1 FROM {pt} p WHERE p.{pk}=c.{ck})"))
RNG = [("loan","original_amount",0,5000000),("loan","interest_rate_at_origination_pct",1,15),("loan","term_months",12,480),("loan","lvr_at_origination_pct",1,105),("loan_monthly_snapshot","interest_rate_pct",1,15),
       ("loan_monthly_snapshot","days_past_due",0,2000),("credit_bureau_report","bureau_score",300,1200),("loan_application","dependants",0,10),("property","bedrooms",1,12),("property","year_built",1850,2026),("ecl_provision_quarterly","lgd",0,1),("ecl_provision_quarterly","pd_12m",0,1)]
for t,c,lo,hi in RNG:
    PROBLEMS.append(P(2, f"Range check: rows in `{t}` where `{c}` is outside {lo} to {hi} (NULLs excluded). Count. One number.",
      f"SELECT COUNT(*) FROM {t} WHERE {c} IS NOT NULL AND ({c} < {lo} OR {c} > {hi})"))
for y in range(2019,2026):
    PROBLEMS.append(P(3, f"Snapshot gaps for loans originated in {y}: loans whose snapshot row count is not `MAX(months_on_book)+1`. Count. One number.",
      f"SELECT COUNT(*) FROM (SELECT s.loan_id FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE {yr('l.origination_date',y)} GROUP BY 1 HAVING COUNT(*)<>MAX(s.months_on_book)+1)"))
