""" test chemkin_io.calculator.mechanism
"""

from __future__ import unicode_literals
from builtins import open
import os
import numpy as np
import chemkin_io


def _read_file(file_name):
    with open(file_name, encoding='utf8', errors='ignore') as file_obj:
        file_str = file_obj.read()
    return file_str


PATH = os.path.dirname(os.path.realpath(__file__))
SYNGAS_PATH = os.path.join(PATH, '../data/syngas')
SYNGAS_MECH_STR = _read_file(os.path.join(SYNGAS_PATH, 'mechanism.txt'))

SYNGAS_REACTION_BLOCK = chemkin_io.parser.util.clean_up_whitespace(
    chemkin_io.parser.mechanism.reaction_block(SYNGAS_MECH_STR))
SYNGAS_REACTION_STRS = chemkin_io.parser.reaction.data_strings(
    SYNGAS_REACTION_BLOCK)
REACTION = SYNGAS_REACTION_STRS[20]

TROE_REACTION = SYNGAS_REACTION_STRS[0]
LINDEMANN_REACTION = SYNGAS_REACTION_STRS[2]
CHEBYSHEV_REACTION = SYNGAS_REACTION_STRS[12]
HIGHP_REACTION = 'CO(1)+O(5)(+M)=CO2(12)(+M)     1.880e+11 0.000     2.430'
PLOG_REACTION = """HOCO<=>CO+OH         6.300E+032    -5.960   32470.0
PLOG/      0.0010     1.550E-008     2.930      8768.0/
PLOG/      0.0030     1.770E+003     0.340     18076.0/
PLOG/      0.0296     2.020E+013    -1.870     22755.0/
PLOG/      0.0987     1.680E+018    -3.050     24323.0/
PLOG/      0.2961     2.500E+024    -4.630     27067.0/
PLOG/      0.9869     4.540E+026    -5.120     27572.0/"""
# print('\n\nRate Data for a Reaction')
# print(REACTION)

# Duplicate Reaction Strings
DUP_HIGHP_REACTION = """CO+OH<=>CO2+H    7.015e+4     2.053          -355.7
CO+OH<=>CO2+H   5.757e+12    -0.664           331.8"""

DUP_PLOG_REACTION = (
    "C2H3+O2<=>C2H3OO  4.07E+27    -4.67   5222\n"
    "PLOG/1.000E-02  1.55E+24    -5.45   9662.0/\n"
    "PLOG/1.000E-01  3.48E+56    -15.01  19160.0/\n"
    "PLOG/3.160E-01  1.25E+64    -16.97  21290.0/\n"
    "PLOG/1.000E+00  3.34E+61    -15.79  20150.0/\n"
    "PLOG/3.160E+00  7.34E+53    -13.11  17300.0/\n"
    "PLOG/1.000E+01  4.16E+48    -11.21  16000.0/\n"
    "PLOG/3.160E+01  2.33E+43    -9.38   14810.0/\n"
    "PLOG/1.000E+02  3.41E+39    -8.04   14360.0/\n"
    "DUP\n"
    "C2H3+O2<=>C2H3OO  4.07E+27    -4.67   5222\n"
    "PLOG/1.000E-02  1.78E-09    4.15    -4707.0/\n"
    "PLOG/1.000E-01  2.36E+22    -4.52   2839.0/\n"
    "PLOG/3.160E-01  2.00E+26    -5.43   2725.0/\n"
    "PLOG/1.000E+00  6.13E+28    -5.89   3154.0/\n"
    "PLOG/3.160E+00  2.14E+29    -5.8    3520.0/\n"
    "PLOG/1.000E+01  3.48E+28    -5.37   3636.0/\n"
    "PLOG/3.160E+01  3.32E+27    -4.95   3610.0/\n"
    "PLOG/1.000E+02  1.03E+27    -4.72   3680.0/\n"
    "DUP\n"
)

# Temperatures and Pressures
T_REF = 1.0
TEMPS = np.array([500.0, 1000.0, 1500.0, 2000.0])
PRESSURES = np.array([1, 5, 10])
PRESSURES2 = np.array([0.0100, 0.0700, 0.987])
PRESSURES3 = np.array([0.1, 0.5, 2])


def test__mechanism():
    """ test chemkin_io.calculator.reaction.reactant_units
        test chemkin_io.calculator.reaction.mechanism
    """
    units = chemkin_io.parser.mechanism.reaction_units(
        SYNGAS_MECH_STR)
    print('units')
    print(units)
    ktp_dct = chemkin_io.calculator.rates.mechanism(
        SYNGAS_REACTION_BLOCK, units, T_REF, TEMPS, pressures=PRESSURES)
    for spc, ktp in ktp_dct.items():
        print(spc)
        print(ktp)


def test__high_p_rate_constants():
    """ test chemkin_io.calculator.rates.reaction
        for a reaction with only high-pressure params
    """
    units = chemkin_io.parser.mechanism.reaction_units(
        SYNGAS_MECH_STR)
    print('units')
    print(units)
    ktp_dct = chemkin_io.calculator.rates.reaction(
        HIGHP_REACTION, units, T_REF, TEMPS, pressures=None)
    print('\nhigh-pressure rate_constants')
    for key, val in ktp_dct.items():
        print(key)
        print(val)


def test__lindemann_rate_constants():
    """ test chemkin_io.calculator.rates.reaction
        for a reaction with high-pressure and low-pressure params
    """
    units = chemkin_io.parser.mechanism.reaction_units(
        SYNGAS_MECH_STR)
    print('units')
    print(units)
    ktp_dct = chemkin_io.calculator.rates.reaction(
        LINDEMANN_REACTION, units, T_REF, TEMPS, pressures=PRESSURES)
    print('\nLindemann rate_constants')
    for key, val in ktp_dct.items():
        print(key)
        print(val)


def test__troe_rate_constants():
    """ test chemkin_io.calculator.rates.reaction
        for a reaction with only high-pressure, low-pressure, and Troe params
    """
    units = chemkin_io.parser.mechanism.reaction_units(
        SYNGAS_MECH_STR)
    ktp_dct = chemkin_io.calculator.rates.reaction(
        TROE_REACTION, units, T_REF, TEMPS, pressures=PRESSURES)
    print('\nTroe rate_constants')
    for key, val in ktp_dct.items():
        print(key)
        print(val)


def test__chebyshev_rate_constants():
    """ test chemkin_io.calculator.rates.reaction
        for a reaction with only high-pressure and Chebyshev params
    """
    units = chemkin_io.parser.mechanism.reaction_units(
        SYNGAS_MECH_STR)
    ktp_dct = chemkin_io.calculator.rates.reaction(
        CHEBYSHEV_REACTION, units, T_REF, TEMPS, pressures=PRESSURES)
    print('\nChebyshev rate_constants')
    for key, val in ktp_dct.items():
        print(key)
        print(val)


def test__plog_rate_constants():
    """ test chemkin_io.calculator.rates.reaction
        for a reaction with only high-pressure and PLog params
    """
    units = ('cal/mole', 'moles')
    ktp_dct = chemkin_io.calculator.rates.reaction(
        PLOG_REACTION, units, T_REF, TEMPS, pressures=PRESSURES2)
    print('\nPLog rate_constants')
    for key, val in ktp_dct.items():
        print(key)
        print(val)


def test__duplicate_high_p_rate_constants():
    """ test chemkin_io.calculator.rates.reaction
        for a reaction with only high-pressure params
        that has a duplicate string
    """
    units = ('cal/mole', 'moles')
    ktp_dct = chemkin_io.calculator.rates.reaction(
        DUP_HIGHP_REACTION, units, T_REF, TEMPS, pressures=None)
    print('\nhigh-pressure rate_constants')
    for key, val in ktp_dct.items():
        print(key)
        print(val)


def test__duplicate_plog_rate_constants():
    """ test chemkin_io.calculator.rates.reaction
    """
    units = ('cal/mole', 'moles')
    ktp_dct = chemkin_io.calculator.rates.reaction(
        DUP_PLOG_REACTION, units, T_REF, TEMPS, pressures=PRESSURES3)
    print('\nplog rate_constants')
    for key, val in ktp_dct.items():
        print(key)
        print(val)


if __name__ == '__main__':
    test__mechanism()
    test__high_p_rate_constants()
    test__lindemann_rate_constants()
    test__troe_rate_constants()
    test__chebyshev_rate_constants()
    test__plog_rate_constants()
    test__duplicate_high_p_rate_constants()
    test__duplicate_plog_rate_constants()
