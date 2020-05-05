""" test chemkin_io.parser.mechanism
"""

from __future__ import unicode_literals
from builtins import open
import os
import numpy
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
TROE1_REACTION = GROUPED_REACTION_STRS[3]
TROE2_REACTION = GROUPED_REACTION_STRS[4]
PLOG_REACTION = GROUPED_REACTION_STRS[5]
DUP_PLOG_REACTION = GROUPED_REACTION_STRS[6]
CHEBYSHEV_REACTION = GROUPED_REACTION_STRS[7]


def test__data_objs():
    """ test chemkin_io.parser.reaction.data_strings
        test chemkin_io.parser.reaction.data_dct
    """

    rxn_strs = chemkin_io.parser.reaction.data_strings(
        FAKE1_REACTION_BLOCK)
    rxn_dct = chemkin_io.parser.reaction.data_dct(
        FAKE1_REACTION_BLOCK)

    print('\ndct')
    for key, val in rxn_dct.items():
        print(key)
        print(val)
    assert len(rxn_strs) == 10
    assert len(rxn_dct) == 8


def test__reactant_names():
    """ test chemkin_io.parser.reaction.reactant_names
    """
    names = chemkin_io.parser.reaction.reactant_names(PLOG_REACTION)
    test_names = ('HOCO',)
    assert names == test_names


def test__product_names():
    """ test chemkin_io.parser.reaction.product_names
    """
    names = chemkin_io.parser.reaction.product_names(PLOG_REACTION)
    test_names = ('CO', 'OH')
    assert names == test_names


def test__high_p_parameters():
    """ test chemkin_io.parser.reaction.high_p_parameters
    """
    params1 = chemkin_io.parser.reaction.high_p_parameters(
        HIGHP_REACTION)
    params2 = chemkin_io.parser.reaction.high_p_parameters(
        DUP_HIGHP_REACTION)
    params3 = chemkin_io.parser.reaction.high_p_parameters(
        LINDEMANN_REACTION)
    params4 = chemkin_io.parser.reaction.high_p_parameters(
        TROE1_REACTION)
    params5 = chemkin_io.parser.reaction.high_p_parameters(
        PLOG_REACTION)
    params6 = chemkin_io.parser.reaction.high_p_parameters(
        DUP_PLOG_REACTION)
    params7 = chemkin_io.parser.reaction.high_p_parameters(
        CHEBYSHEV_REACTION)
    print('\nhigh-pressure parameters')
    print(params1)
    print(params2)
    print(params3)
    print(params4)
    print(params5)
    print(params6)
    print(params7)

    test_params1 = [24100000000000.0, 0.0, 3970.0]
    test_params2 = [1740000000000.0, 0.0, 318.0]
    test_params3 = [4650000000000.0, 0.44, 0.0]
    test_params4 = [2000000000000.0, 0.9, 48749.0]
    test_params5 = [6.3e+32, -5.96, 32470.0]
    test_params6 = [1770000000000.0, 0.16, 4206]
    test_params7 = [1.0, 0.0, 0.0]

    assert numpy.allclose(params1, test_params1)
    assert numpy.allclose(params2, test_params2)
    assert numpy.allclose(params3, test_params3)
    assert numpy.allclose(params4, test_params4)
    assert numpy.allclose(params5, test_params5)
    assert numpy.allclose(params6, test_params6)
    assert numpy.allclose(params7, test_params7)


def test__low_p_parameters():
    """ test chemkin_io.parser.reaction.low_p_parameters
    """
    params1 = chemkin_io.parser.reaction.low_p_parameters(
        LINDEMANN_REACTION)
    params2 = chemkin_io.parser.reaction.low_p_parameters(
        TROE1_REACTION)
    params3 = chemkin_io.parser.reaction.low_p_parameters(
        TROE2_REACTION)

    test_params1 = [1.737e+19, -1.23, 0.0]
    test_params2 = [2.49e+24, -2.3, 48749.0]
    test_params3 = [2.49e+24, -2.3, 48.75]

    assert numpy.allclose(params1, test_params1)
    assert numpy.allclose(params2, test_params2)
    assert numpy.allclose(params3, test_params3)


def test__troe_parameters():
    """ test chemkin_io.parser.reaction.troe_parameters
    """
    params1 = chemkin_io.parser.reaction.troe_parameters(
        TROE1_REACTION)
    params2 = chemkin_io.parser.reaction.troe_parameters(
        TROE2_REACTION)

    test_params1 = [0.43, 1e-30, 1e+30, None]
    test_params2 = [0.58, 30.0, 90000.0, 90000.0]

    assert numpy.allclose(params1[0:3], test_params1[0:3])
    assert params1[3] is None and test_params1[3] is None
    assert numpy.allclose(params2, test_params2)


def test__buffer_enhance_factors():
    """ test chemkin_io.parser.reaction.buffer_enhance_factors
    """
    # collider to lindemann
    fct_dct1 = chemkin_io.parser.reaction.buffer_enhance_factors(
        TROE1_REACTION)
    fct_dct2 = chemkin_io.parser.reaction.buffer_enhance_factors(
        TROE2_REACTION)
    print('\nLow Pressure Buffer Enhhancement Factors')
    print(fct_dct1)
    print(fct_dct2)


def test__plog_parameters():
    """ test chemkin_io.parser.reaction.plog_parameters
    """
    params1 = chemkin_io.parser.reaction.plog_parameters(
        PLOG_REACTION)
    params2 = chemkin_io.parser.reaction.plog_parameters(
        DUP_PLOG_REACTION)

    test_params1 = {
        0.001: [1.55e-08, 2.93, 8768.0],
        0.003: [1770.0, 0.34, 18076.0],
        0.0296: [20200000000000.0, -1.87, 22755.0],
        0.0987: [1.68e+18, -3.05, 24323.0],
        0.2961: [2.5e+24, -4.63, 27067.0],
        0.9869: [4.54e+26, -5.12, 27572.0],
        2.9607: [7.12e+28, -5.6, 28535.0],
        9.869: [5.48e+29, -5.7, 28899.0],
        29.607: [9.89e+31, -6.19, 30518.0],
        98.69: [5.74e+33, -6.53, 32068.0],
        296.07: [2.61e+33, -6.29, 32231.0],
        986.9: [6.3e+32, -5.96, 32470.0]
    }

    test_params2 = {
        0.01: [13600000000.0, 0.62, -277.6],
        0.1: [14200000000.0, 0.62, -247.7],
        0.316: [16600000000.0, 0.6, -162.5],
        1.0: [20200000000.0, 0.58, 38.4],
        3.16: [9750000000.0, 0.67, 248.0],
        10.0: [7340000000.0, 0.72, 778.1],
        31.6: [1570000000.0, 0.92, 1219.0],
        100.0: [78500000.0, 1.28, 1401.0]
    }


def test__chebyshev_parameters():
    """ test chemkin_io.parser.reaction.chebyshev_parameters
    """
    params = chemkin_io.parser.reaction.chebyshev_parameters(
        CHEBYSHEV_REACTION)
    print('\nChebyshev parameters')
    print(params)

    test_params = {
        't_limits': [300.0, 2200.0],
        'p_limits': [0.01, 98.702],
        'alpha_dim': [6, 4],
        'alpha_elm': [[8.684, 8.684, 1.879e-15, 1.879e-15],
                      [-0.2159, -0.2159, 2.929e-17, 2.929e-17],
                      [-1.557e-15, -1.557e-15, -8.346e-31, -8.346e-31],
                      [0.2159, 0.2159, -2.929e-17, -2.929e-17],
                      [-2.684, -2.684, -1.879e-15, -1.879e-15],
                      [0.2159, 0.2159, -2.929e-17, -2.929e-17]]
    }


if __name__ == '__main__':
    test__data_objs()
    test__reactant_names()
    test__product_names()
    test__high_p_parameters()
    test__low_p_parameters()
    test__troe_parameters()
    test__buffer_enhance_factors()
    test__plog_parameters()
    test__chebyshev_parameters()
