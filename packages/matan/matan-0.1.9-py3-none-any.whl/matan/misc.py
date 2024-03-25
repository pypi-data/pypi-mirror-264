from math import log10, floor


def round_significant(x: float, significant: int = 2):
    """round the number with x significant digits

    Parameters
    ----------
    x : float
        number to round
    significant : int
        how many significant digits to include

    Examples
    --------
    FIXME: Add docs.

    """
    try:
        return round(x, significant - int(floor(log10(abs(x)))) - 1)
    except ValueError:
        return x
