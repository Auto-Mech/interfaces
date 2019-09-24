"""
Functions to fit rate constants to Single or Double Arrhenius Functions
Performs fits either using SciPy or SJK's dsarrfit code
"""

from ratefit.fit import arrhenius
from ratefit.fit.util import get_valid_tk


__all__ = [
    'arrhenius',
    'get_valid_tk',
]
