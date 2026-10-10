"""Shared stage: form answers in, one row of engineered raw inputs out.

Skeleton drafted by AI. Function bodies marked TODO are for Chuch to write.
The config files in ../config hold every rule, so nothing here is hardcoded.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def load_config(name):
    """Read one config file, e.g. load_config('loan_terms')."""
    
    with open(CONFIG_DIR / f"{name}.json") as fh:
        
        return json.load(fh)


def years_to_days(years):
    """Years employed -> DAYS_EMPLOYED. Blank input returns NaN.
    Rule: employment_rules.json, 'years_to_days'."""
    
    return np.nan if pd.isna(years) else -(years * 365.25)


def ext_value(field, band_label):
    bands = load_config('ext_score_bands')

    if band_label == bands['missing_label']:             # 1
        return np.nan                    # 2

    for band in bands['fields'][field]['bands']:
        if band['label'] == band_label:      # 3
            return band['value']          # 4

    raise ValueError(f"Unknown band '{band_label}' for {field}")           # name the field and the label in the message


def repayment(loan_amount, term_months):
    """Monthly repayment from amount, term and the assumed rate.
    Formula and rate: loan_terms.json, 'repayment'."""
    
    terms = load_config('loan_terms')
    
    rate = terms['repayment']['assumed_rate_pa'] / 12       # convert to monthly rate
    
    payment = loan_amount * ((rate * (1 + rate)**term_months) / ((1 + rate)**term_months - 1))
    
    return payment


def safe_div(num, den):
    """Same rule as the driver scan: zero or blank denominator returns NaN."""
    
    return np.nan if pd.isna(den) or den == 0 else num / den
    
    


def org_band(option_label):
    """Plain-language organisation option -> ORG_BAND level.
    Table: organisation_options.json."""
    
    org_bands = load_config('organisation_options')
    
    for org in org_bands['options']:
        if org['label'] == option_label:
            return org['org_band']
    


def engineer(form):
    """form: dict of answers from the app.
    Returns a one-row DataFrame holding the columns every scorecard needs:
    EXT_SOURCE_1/2/3, DAYS_EMPLOYED, ANNUITY_CREDIT, AMT_GOODS_PRICE,
    CREDIT_GOODS, ORG_BAND, plus the categorical fields passed straight through.
    """
    # TODO
