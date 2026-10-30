def P(level, text, code, tables, order=None, hint=None, tol=0.011, empty_ok=False):
    """One problem. `code` is the reference solution and must assign `result`.
    `tables` are loaded into variables before the code runs (loan_monthly_snapshot -> snap,
    loan_application -> app, application_assessment -> assess, application_applicant -> applicant,
    credit_bureau_report -> bureau; everything else keeps its table name)."""
    return dict(level=level, text=text.strip(), code=code.strip(), tables=list(tables), order=order,
                hint=hint, tol=tol, empty_ok=empty_ok)
