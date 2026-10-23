"""Stage 01: join orig + perf, derive vintage quarter and MOB, first-event default/prepay flags, sanity checks."""

import pandas as pd
import numpy as np
import os
import sys

from freddie.config import DEFAULT_ZBC, PREPAY_ZBC, CENSOR_ZBC



# Add Vintage Quarter


def add_mob(df, orig_df):
    """Add months on book (``mob``) to the loan-month panel.

    MOB counts months from the loan's first payment date to the reporting
    period, plus one, so it matches ``loan_age`` on unmodified loans.
    ``loan_age`` is not used as the clock because Freddie Mac restarts it
    after a loan modification (User Guide, LOAN AGE), which puts a modified
    loan's months out of time order.

    Parameters
    ----------
    df : pandas.DataFrame
        Loan-month panel with ``loan_id`` and ``period`` (YYYYMM).
    orig_df : pandas.DataFrame
        Origination frame with ``loan_id`` and ``first_payment_date`` (YYYYMM).

    Returns
    -------
    pandas.DataFrame
        ``df`` with an integer ``mob`` column.
    """
    
    first_payment = df['loan_id'].map(orig_df.set_index('loan_id')['first_payment_date'])

    period = pd.to_datetime(df['period'], format='%Y%m')
    first_payment = pd.to_datetime(first_payment, format='%Y%m')

    df['mob'] = (period.dt.year - first_payment.dt.year) * 12 + (period.dt.month - first_payment.dt.month) + 1

    return df

def vintage_quarter(df):
    """Add the origination quarter (``vintage``) from the loan ID.

    Freddie Mac encodes the origination quarter in the loan sequence number,
    so ``F06Q10000059`` becomes ``2006Q1``.

    Parameters
    ----------
    df : pandas.DataFrame
        Any frame with a ``loan_id`` column.

    Returns
    -------
    pandas.DataFrame
        ``df`` with a ``vintage`` column, e.g. ``"2006Q1"``.
    """
    
    df['vintage'] = df['loan_id'].str.replace(r'^F(\d{2})(Q[1-4]).*', r'20\1\2', regex=True)
    
    return df


def default_flagger(df):
    """Flag each loan-month in which a default trigger fires.

    A month is flagged when any of these holds:

    - delinquency status is ``"03"`` or higher (90+ days past due)
    - delinquency status is ``"RA"`` (REO acquisition)
    - the zero balance code is a loss code (02, 03, 09, 15)

    This marks the trigger month only. A loan that cures drops back to 0;
    ``default_flag_absorbing`` makes the flag permanent.

    Parameters
    ----------
    df : pandas.DataFrame
        Loan-month panel with ``current_dlq_status`` and ``zero_balance_code``.

    Returns
    -------
    pandas.DataFrame
        ``df`` with a 0/1 ``default_flag`` column.
    """
    
    loss_codes = ['02', '03', '09', '15']
    
    status_str = df["current_dlq_status"].astype(str)
    
    is_numeric_gte_03 = status_str.str.isdigit() & (
    status_str >= "03"
)
    is_ra = status_str == "RA"

    is_zbc_loss = df['zero_balance_code'].isin(loss_codes)

    
    df['default_flag'] = np.select(condlist=[is_numeric_gte_03 | is_ra | is_zbc_loss], choicelist=[1], default=0)
    
    return df


def default_flag_absorbing(df):
    """Make default an absorbing state: once defaulted, always defaulted.

    Sorts each loan's months by ``mob`` and carries the first default
    trigger forward with a running maximum, so later months stay flagged
    even if the borrower catches up. This keeps cumulative default curves
    from falling.

    Parameters
    ----------
    df : pandas.DataFrame
        Loan-month panel with ``loan_id``, ``mob`` and ``default_flag``.

    Returns
    -------
    pandas.DataFrame
        A sorted copy of ``df`` with a 0/1 ``default_flag_absorbing`` column.
    """
    
    df = df.sort_values(['loan_id', 'mob'])   # mob, not loan_age (Edited by AI)
    
    df['default_flag_absorbing'] = df.groupby('loan_id')['default_flag'].cummax()
    
    return df


def prepay_flag(df):
    """Flag the month a loan was paid off in full (zero balance code 01).

    Prepayment only counts if the loan had not already defaulted, because
    default is absorbing and takes priority. Prepaid loans stay in the
    vintage denominator as a competing risk.

    Parameters
    ----------
    df : pandas.DataFrame
        Loan-month panel with ``zero_balance_code`` and
        ``default_flag_absorbing``.

    Returns
    -------
    pandas.DataFrame
        ``df`` with a 0/1 ``prepay_flag`` column.
    """
    
    
    df['prepay_flag'] = ((df['zero_balance_code'] == '01') & (df['default_flag_absorbing'] == 0)).astype(int)

    
    return df



def censor_flag(df):
    """Flag the month a loan left the data for a non-credit reason.

    Zero balance codes 16 (re-performing loan securitisation) and 96
    (repurchase for an underwriting defect) end observation without a
    default or a prepayment, so the loan is censored. Only counts if the
    loan had not already defaulted.

    Parameters
    ----------
    df : pandas.DataFrame
        Loan-month panel with ``zero_balance_code`` and
        ``default_flag_absorbing``.

    Returns
    -------
    pandas.DataFrame
        ``df`` with a 0/1 ``censor_flag`` column.
    """
    
    df['censor_flag'] = ((df['zero_balance_code'].isin(['16','96'])) & (df['default_flag_absorbing'] == 0)).astype(int)
    
    return df



def summarise_loans(df):
    """Collapse the loan-month panel into one row per loan.

    For each loan, records when it was written, what happened to it first,
    and when. Priority order is default, then prepaid, then censored;
    a loan with none of these is still open at the data cut-off.

    Parameters
    ----------
    df : pandas.DataFrame
        Flagged loan-month panel with ``loan_id``, ``mob``, ``vintage``,
        ``default_flag``, ``prepay_flag`` and ``censor_flag``.

    Returns
    -------
    pandas.DataFrame
        Indexed by ``loan_id``, with columns:

        - ``vintage``: origination quarter
        - ``last_mob``: last month observed (handles right truncation)
        - ``default_mob``: first default month, NaN if never defaulted
        - ``prepay_mob``: payoff month, NaN if not prepaid
        - ``censor_mob``: censoring month, NaN if not censored
        - ``first_event``: ``"default"``, ``"prepaid"``, ``"censored"`` or ``"open"``
        - ``event_mob``: MOB of ``first_event``, NaN if open
    """

    # Edited by AI: all event months use mob, not loan_age
    
    # last_mob
    
    last_mob = df.groupby('loan_id')['mob'].max()
    
    # default_mob
    
    default_mob = df.query('default_flag == 1').groupby('loan_id')['mob'].min()
    
    # prepay_mob
    
    prepay_mob = df.query('prepay_flag == 1').groupby('loan_id')['mob'].max()
    
    # censor_mob
    
    censor_mob = df.query('censor_flag == 1').groupby('loan_id')['mob'].max()
    
    # vintage
    
    vintage = df.groupby('loan_id')['vintage'].first()
    
    # build_table via concat
    
    loan_table = pd.concat({
    'vintage': vintage,
    'last_mob': last_mob,
    'default_mob': default_mob,
    'prepay_mob': prepay_mob,
    'censor_mob': censor_mob,
                                }, axis=1)
    
    conditions = [loan_table['default_mob'].notna(),
              loan_table['prepay_mob'].notna(),
              loan_table['censor_mob'].notna()]
    
    loan_table['first_event'] = np.select(
        condlist = conditions, 
        choicelist = ['default', 'prepaid', 'censored'], 
        default='open')
    
    loan_table['event_mob'] = np.select(
        condlist = conditions, 
        choicelist = [loan_table['default_mob'], loan_table['prepay_mob'], loan_table['censor_mob']], 
        default=np.nan)
    
    return loan_table