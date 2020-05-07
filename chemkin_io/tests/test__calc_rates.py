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


# Set paths
PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PATH, 'data')
FAKE1_MECH_NAME = 'fake_mech1.txt'

# Read mechanism files
FAKE1_MECH_STR = _read_file(
    os.path.join(DATA_PATH, FAKE1_MECH_NAME))

# Build the reactions blocks and data strings
FAKE1_REACTION_BLOCK = chemkin_io.parser.util.clean_up_whitespace(
    chemkin_io.parser.mechanism.reaction_block(FAKE1_MECH_STR))
FAKE1_REACTION_STRS = chemkin_io.parser.reaction.data_strings(
    FAKE1_REACTION_BLOCK)
FAKE1_REACTION_DCT = chemkin_io.parser.reaction.data_dct(
    FAKE1_REACTION_BLOCK)

# Set the reactions to elements of the string, use dct to have DUPs together
GROUPED_REACTION_STRS = list(FAKE1_REACTION_DCT.values())
HIGHP_REACTION = GROUPED_REACTION_STRS[0]
DUP_HIGHP_REACTION = GROUPED_REACTION_STRS[1]
LINDEMANN_REACTION = GROUPED_REACTION_STRS[2]
TROE_REACTION = GROUPED_REACTION_STRS[3]
PLOG_REACTION = GROUPED_REACTION_STRS[5]
DUP_PLOG_REACTION = GROUPED_REACTION_STRS[6]
CHEBYSHEV_REACTION = GROUPED_REACTION_STRS[7]

# Set temperatures and pressures
T_REF = 1.0
UNITS = ('cal/mole', 'moles')
TEMPS = np.array([500.0, 1000.0, 1500.0, 2000.0])
PRESSURES = np.array([1, 5, 10])
PRESSURES2 = np.array([0.0100, 0.0700, 0.987])
PRESSURES3 = np.array([0.1, 0.5, 2])


def test__high_p_rate_constants():
    """ test chemkin_io.calculator.rates.reaction
        for a reaction with only high-pressure params
    """
    ktp_dct = chemkin_io.calculator.rates.reaction(
        HIGHP_REACTION, UNITS, T_REF, TEMPS, pressures=None)
    print('\nhigh-pressure rate_constants')
    for key, val in ktp_dct.items():
        print(key)
        print(val)
    ktp_dct = chemkin_io.calculator.rates.reaction(
        DUP_HIGHP_REACTION, UNITS, T_REF, TEMPS, pressures=None)
    print('\nhigh-pressure rate_constants')
    for key, val in ktp_dct.items():
        print(key)
        print(val)


def test__lindemann_rate_constants():
    """ test chemkin_io.calculator.rates.reaction
        for a reaction with high-pressure and low-pressure params
    """
    ktp_dct = chemkin_io.calculator.rates.reaction(
        LINDEMANN_REACTION, UNITS, T_REF, TEMPS, pressures=PRESSURES)
    print('\nLindemann rate_constants')
    for key, val in ktp_dct.items():
        print(key)
        print(val)


def test__troe_rate_constants():
    """ test chemkin_io.calculator.rates.reaction
        for a reaction with only high-pressure, low-pressure, and Troe params
    """
    ktp_dct = chemkin_io.calculator.rates.reaction(
        TROE_REACTION, UNITS, T_REF, TEMPS, pressures=PRESSURES)
    print('\nTroe rate_constants')
    for key, val in ktp_dct.items():
        print(key)
        print(val)


def test__chebyshev_rate_constants():
    """ test chemkin_io.calculator.rates.reaction
        for a reaction with only high-pressure and Chebyshev params
    """
    ktp_dct = chemkin_io.calculator.rates.reaction(
        CHEBYSHEV_REACTION, UNITS, T_REF, TEMPS, pressures=PRESSURES)
    print('\nChebyshev rate_constants')
    for key, val in ktp_dct.items():
        print(key)
        print(val)


def test__plog_rate_constants():
    """ test chemkin_io.calculator.rates.reaction
        for a reaction with only high-pressure and PLog params
    """
    ktp_dct = chemkin_io.calculator.rates.reaction(
        PLOG_REACTION, UNITS, T_REF, TEMPS, pressures=PRESSURES2)
    print('\nPLog rate_constants')
    for key, val in ktp_dct.items():
        print(key)
        print(val)
    ktp_dct = chemkin_io.calculator.rates.reaction(
        DUP_PLOG_REACTION, UNITS, T_REF, TEMPS, pressures=PRESSURES3)
    print('\nplog rate_constants')
    for key, val in ktp_dct.items():
        print(key)
        print(val)


def test__mechanism():
    """ test chemkin_io.calculator.reaction.mechanism
    """
    ktp_dct = chemkin_io.calculator.rates.mechanism(
        FAKE1_REACTION_BLOCK, UNITS, T_REF, TEMPS, pressures=PRESSURES)
    for spc, ktp in ktp_dct.items():
        print(spc)
        print(ktp)


def test__branching_ratios():
    """ test chemkin_io.calculator.reaction.branching_ratios
    """
    tot_dct, branch_dct = chemkin_io.calculator.rates.branching_ratios(
        FAKE1_REACTION_BLOCK, UNITS, T_REF, TEMPS, pressures=PRESSURES)
    for spc, ktp in tot_dct.items():
        print(spc)
        print(ktp)
    print('\n\n')
    for spc, ktp in branch_dct.items():
        print(spc)
        print(ktp)


if __name__ == '__main__':
    test__high_p_rate_constants()
    test__lindemann_rate_constants()
    test__troe_rate_constants()
    test__plog_rate_constants()
    test__chebyshev_rate_constants()
    test__mechanism()
    test__branching_ratios()
