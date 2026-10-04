from ._gen import *
MORE_FOR = '12_set_operations'
PROBLEMS = []
for y in range(2019,2025):
    PROBLEMS.append(P(2, f"INTERSECT: customers who lodged an application in {y} AND in {y+1} (primary). Count. One number.",
      f"SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan_application WHERE {yr('application_date',y)} INTERSECT SELECT primary_customer_id FROM loan_application WHERE {yr('application_date',y+1)})"))
for y in range(2019,2025):
    PROBLEMS.append(P(2, f"EXCEPT: customers who applied in {y} but did NOT apply in {y+1}. Count. One number.",
      f"SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan_application WHERE {yr('application_date',y)} EXCEPT SELECT primary_customer_id FROM loan_application WHERE {yr('application_date',y+1)})"))
pairs=[(a,b) for i,a in enumerate(EXT_PURPOSES) for b in EXT_PURPOSES[i+1:]]
for a,b in pairs[:6]:
    PROBLEMS.append(P(2, f"Customers (primary) with BOTH a `'{a}'` and a `'{b}'` loan: count via `INTERSECT`. One number.",
      f"SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan WHERE purpose='{a}' INTERSECT SELECT primary_customer_id FROM loan WHERE purpose='{b}')"))
for c in CHANNELS:
    PROBLEMS.append(P(3, f"Customers with a loan via `'{c}'` but none via any other channel (`EXCEPT`). Count. One number.",
      f"SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan WHERE channel='{c}' EXCEPT SELECT primary_customer_id FROM loan WHERE channel<>'{c}')"))
for y in (2020,2022,2024):
    PROBLEMS.append(P(2, f"`UNION ALL` of two periods: loan counts per `channel` for {y} and {y+1} in one table with a `yr` column. `yr`, `channel`, `loans`; sorted by yr, channel.",
      f"SELECT yr, channel, n FROM (SELECT {y} AS yr, channel, COUNT(*) AS n FROM loan WHERE {yr('origination_date',y)} GROUP BY 2 UNION ALL SELECT {y+1}, channel, COUNT(*) FROM loan WHERE {yr('origination_date',y+1)} GROUP BY 2) ORDER BY 1,2"))
PROBLEMS += [
 P(3, "Loans closed by refinance elsewhere that never had a retention discount event (EXCEPT of loan_ids). Count. One number.",
   "SELECT COUNT(*) FROM (SELECT loan_id FROM loan WHERE closure_reason='Refinanced to another lender' EXCEPT SELECT loan_id FROM loan_event WHERE event_type='Retention discount applied')"),
 P(3, "Customers who were declined at least once but later have a loan: `INTERSECT` declined customers with loan customers. Count. One number.",
   "SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan_application WHERE decision='Declined' INTERSECT SELECT primary_customer_id FROM loan)"),
]
