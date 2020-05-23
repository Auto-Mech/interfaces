""" Physical constants and conversion factors
"""

from qcelemental import constants as qcc

# physical constants
NAVO = 6.0221409e+23
RC = 1.98720425864083e-3  # gas constant R in kcal/mol.K

# conversion factors
CAL2KCAL = qcc.conversion_factor('cal/mol', 'kcal/mol')
J2KCAL = qcc.conversion_factor('J/mol', 'kcal/mol')
KJ2KCAL = qcc.conversion_factor('kJ/mol', 'kcal/mol')
KEL2KCAL = qcc.conversion_factor('kelvin', 'kcal/mol')
