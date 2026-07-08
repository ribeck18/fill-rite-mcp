class FillriteError(Exception):
    """Base for all Fillrite problems."""


class FillriteAuthError(FillriteError):
    """Auth was rejected - token expired or credientials are wrong. Needs re-auth."""


class FillriteResponseError(FillriteError):
    """Fillrite returned something we can't parse or didn't expect."""
