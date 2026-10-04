def P(level, text, sql, order=None, hint=None, tol=0.011, empty_ok=False, title=None):
    return dict(level=level, text=text.strip(), sql=sql.strip(), order=order, hint=hint, tol=tol, empty_ok=empty_ok, title=title)
