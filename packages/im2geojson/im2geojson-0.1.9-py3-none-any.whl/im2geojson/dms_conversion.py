"""
Convert latitude / longitude DMS representation to decimal.
"""
from decimal import Decimal, getcontext
getcontext().prec = 9

SIX_PLACES = Decimal(10) **-6 
NORTH_REF = 'N'
SOUTH_REF = 'S'
EAST_REF = 'E'
WEST_REF = 'W'
MAX_MINUTES = 59
MAX_SECONDS = 59
MAX_LAT_DEGREES = 90
MAX_LONG_DEGREES = 180


def is_latitude(ref):
    """bool: Return True if `ref` is 'N' or 'S'."""
    return (ref == NORTH_REF or ref == SOUTH_REF)

def is_longitude(ref):
    """bool: Return True if `ref` is 'E' or 'W'."""
    return (ref == EAST_REF or ref == WEST_REF)

def dms_to_decimal(deg, min, sec, ref):
    """
    Convert degrees, minutes, seconds and reference to decimal.

    Parameters
    ----------
    deg : float
        Degrees.
    min : float
        Minutes.
    sec : float
        Seconds 
    ref : str
        The compass reference.
 
    Returns
    -------
    float
        Decimal degree as float.

    Raises
    ------
    ValueError
        Invalid GPS Reference, Expecting N, S, E or W.
        Invalid Seconds, Should be positive and less than 60.
        Invalid Minutes, Should be positive and less than 60.
        Invalid Degrees, Should be positive.
        Invalid Latitude, cannot be greater than 90 degrees.
        Invalid Longitude, cannot be greater than 180 degrees.
    """
    if ref not in [NORTH_REF, SOUTH_REF, EAST_REF, WEST_REF]:
        raise ValueError(f'ValueError: Invalid GPS Reference {ref}, Expecting N, S, E or W')
    
    if sec > MAX_SECONDS or sec < 0:
        raise ValueError(f'ValueError: Invalid Seconds {str(sec)}, Should be positive and less than 60')
    
    if min > MAX_MINUTES or min < 0:
        raise ValueError(f'ValueError: Invalid Minutes {str(min)}, Should be positive and less than 60')
    
    if deg < 0:
        raise ValueError(f'ValueError: Invalid Degrees {str(sec)}, Should be positive')
    
    if is_latitude(ref) and deg > MAX_LAT_DEGREES:
        raise ValueError(f'ValueError: Invalid Latitude {str(deg) + ref}, cannot be greater than 90 degrees')
    
    elif is_longitude(ref) and deg > MAX_LONG_DEGREES:
        raise ValueError(f'ValueError: Invalid Longitude {str(deg) + ref}, cannot be greater than 180 degrees')
    
    sign = (-1 if ref == SOUTH_REF or ref == WEST_REF else 1)
    dec_deg = (Decimal(deg) + Decimal(min)/Decimal(60) + Decimal(sec)/Decimal(3600)) * sign

    return float(dec_deg.quantize(SIX_PLACES))
