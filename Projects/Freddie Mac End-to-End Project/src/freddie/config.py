"""Shared settings: project paths (via find_repo_root), RAW_DIR = <repo>/Datasets/Freddie Mac Vintage Data (sample_YYYY.zip -> sample_orig_YYYY.txt, sample_perf_YYYY.txt), YEARS = [2006, 2007, 2010, 2016], column names and dtypes, default/prepay code lists, segment band edges, fixed MOBs."""
from pathlib import Path

RAW_DIR = Path(r"C:\Dev\CreditRiskLearning\Projects\Freddie Mac End-to-End Project\data\raw")
INTERIM_DIR = Path(r"C:\Dev\CreditRiskLearning\Projects\Freddie Mac End-to-End Project\data\interim")

ORIG_COLS = [
        "credit_score",                  # 1  Classic FICO
        "first_payment_date",            # 2
        "first_time_homebuyer",          # 3
        "maturity_date",                 # 4
        "msa",                           # 5
        "mi_pct",                        # 6
        "num_units",                     # 7
        "occupancy_status",              # 8
        "orig_cltv",                     # 9
        "orig_dti",                      # 10
        "orig_upb",                      # 11
        "orig_ltv",                      # 12
        "orig_interest_rate",            # 13
        "channel",                       # 14
        "prepayment_penalty_flag",       # 15
        "amortization_type",             # 16
        "property_state",                # 17
        "property_type",                 # 18
        "postal_code",                   # 19
        "loan_id",                       # 20 Loan Identifier (join key)
        "loan_purpose",                  # 21
        "orig_loan_term",                # 22
        "num_borrowers",                 # 23
        "seller_name",                   # 24
        "super_conforming_flag",         # 25
        "pre_harp_loan_id",              # 26
        "special_eligibility_program",   # 27
        "harp_flag",                     # 28
        "property_valuation_method",     # 29
        "interest_only_flag",            # 30
        "vantage_score",                 # 31 VantageScore 4.0
    ]
        
ORIG_DTYPES = {
        "credit_score": "Int64",
        "first_payment_date": "string",          # YYYYMM, convert in stage 01
        "first_time_homebuyer": "category",
        "maturity_date": "string",
        "msa": "string",                         # code, not a quantity
        "mi_pct": "Int64",
        "num_units": "Int64",
        "occupancy_status": "category",
        "orig_cltv": "Int64",
        "orig_dti": "Int64",
        "orig_upb": "Int64",
        "orig_ltv": "Int64",
        "orig_interest_rate": "float64",
        "channel": "category",
        "prepayment_penalty_flag": "category",
        "amortization_type": "category",
        "property_state": "category",
        "property_type": "category",
        "postal_code": "string",                 # code; looks numeric but don't treat it as a number
        "loan_id": "string",
        "loan_purpose": "category",
        "orig_loan_term": "Int64",
        "num_borrowers": "Int64",
        "seller_name": "category",
        "super_conforming_flag": "category",
        "pre_harp_loan_id": "string",
        "special_eligibility_program": "category",
        "harp_flag": "category",
        "property_valuation_method": "category", # 1/2/3/9 codes
        "interest_only_flag": "category",
        "vantage_score": "Int64",                # blank for older loans
    }

PERF_COLS = [
        "loan_id",                           # 1  join key
        "period",                            # 2  YYYYMM
        "current_upb",                       # 3
        "current_dlq_status",                # 4  00, 01, 02... or RA
        "loan_age",                          # 5
        "remaining_months",                  # 6  to legal maturity
        "defect_settlement_date",            # 7
        "modification_flag",                 # 8
        "zero_balance_code",                 # 9
        "zero_balance_date",                 # 10
        "current_interest_rate",             # 11
        "current_non_int_bearing_upb",       # 12
        "ddlpi",                             # 13 due date of last paid instalment
        "mi_recoveries",                     # 14
        "net_sales_proceeds",                # 15
        "non_mi_recoveries",                 # 16
        "total_expenses",                    # 17
        "legal_costs",                       # 18
        "maintenance_costs",                 # 19
        "taxes_and_insurance",               # 20
        "misc_expenses",                     # 21
        "actual_loss",                       # 22
        "cumulative_mod_costs",              # 23
        "rate_step_flag",                    # 24
        "payment_deferral_flag",             # 25
        "eltv",                              # 26 estimated LTV
        "zero_balance_removal_upb",          # 27
        "dlq_accrued_interest",              # 28
        "dlq_due_to_disaster",               # 29
        "borrower_assistance_plan",          # 30
        "current_period_mod_costs",          # 31
        "current_int_bearing_upb",           # 32
        "mi_cancellation_flag",              # 33
        "servicer_name",                     # 34
        "bankruptcy_cramdown_costs",         # 35
    ]

PERF_DTYPES = {
        "loan_id": "string",
        "period": "string",                        # YYYYMM, convert in stage 01
        "current_upb": "float64",
        "current_dlq_status": "category",          # text: keeps "00" and "RA"
        "loan_age": "Int64",
        "remaining_months": "Int64",
        "defect_settlement_date": "string",
        "modification_flag": "category",
        "zero_balance_code": "category",           # "01", "03"... text keeps the leading zero
        "zero_balance_date": "string",
        "current_interest_rate": "float64",
        "current_non_int_bearing_upb": "float64",
        "ddlpi": "string",
        "mi_recoveries": "float64",
        "net_sales_proceeds": "string",            # can be "C" or "U", not just numbers
        "non_mi_recoveries": "float64",
        "total_expenses": "float64",
        "legal_costs": "float64",
        "maintenance_costs": "float64",
        "taxes_and_insurance": "float64",
        "misc_expenses": "float64",
        "actual_loss": "float64",
        "cumulative_mod_costs": "float64",
        "rate_step_flag": "category",
        "payment_deferral_flag": "category",
        "eltv": "Int64",                           # 999 = unknown
        "zero_balance_removal_upb": "float64",
        "dlq_accrued_interest": "float64",
        "dlq_due_to_disaster": "category",
        "borrower_assistance_plan": "category",
        "current_period_mod_costs": "float64",
        "current_int_bearing_upb": "float64",
        "mi_cancellation_flag": "category",
        "servicer_name": "category",
        "bankruptcy_cramdown_costs": "float64",
    }

PERF_KEEP = [
        "loan_id",
        "period",
        "current_upb",
        "current_dlq_status",
        "loan_age",
        "zero_balance_code",
        "zero_balance_date",
    ]