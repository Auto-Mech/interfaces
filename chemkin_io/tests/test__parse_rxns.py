""" test chemkin_io.parser.mechanism
"""

from __future__ import unicode_literals
from builtins import open
import os
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

# Set the reactions to elements of the string
HIGHP_REACTION = FAKE1_REACTION_STRS[0]
DUP_HIGHP_REACTION = FAKE1_REACTION_STRS[1]
LINDEMANN_REACTION = FAKE1_REACTION_STRS[2]
TROE_REACTION = FAKE1_REACTION_STRS[3]
PLOG_REACTION = FAKE1_REACTION_STRS[4]
DUP_PLOG_REACTION = FAKE1_REACTION_STRS[5]
CHEBYSHEV_REACTION = FAKE1_REACTION_STRS[6]


def test__data_strings():
    """ test chemkin_io.parser.reaction.data_strings
    """

    rxn_strs = chemkin_io.parser.reaction.data_strings(
        FAKE1_REACTION_BLOCK)
    assert len(rxn_strs) == 9


def test__reactant_names():
    """ test chemkin_io.parser.reaction.reactant_names
    """
    names = chemkin_io.parser.reaction.reactant_names(PLOG_REACTION)
    print('\nreactants')
    print(names)


def test__product_names():
    """ test chemkin_io.parser.reaction.product_names
    """
    names = chemkin_io.parser.reaction.product_names(PLOG_REACTION)
    print('\nproducts')
    print(names)


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
        TROE_REACTION)
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
    # could pull from all


def test__low_p_parameters():
    """ test chemkin_io.parser.reaction.low_p_parameters
    """
    print(LINDEMANN_REACTION)
    print('')
    print(TROE_REACTION)
    params1 = chemkin_io.parser.reaction.low_p_parameters(
        LINDEMANN_REACTION)
    params2 = chemkin_io.parser.reaction.low_p_parameters(
        TROE_REACTION)
    print('\nlow-pressure parameters')
    print(params1)
    print(params2)
    # could pull from low and troe


def test__troe_parameters():
    """ test chemkin_io.parser.reaction.troe_parameters
    """
    params = chemkin_io.parser.reaction.troe_parameters(
        TROE_REACTION)
    print('\nTroe parameters')
    print(params)


def test__buffer_enhance_factors():
    """ test chemkin_io.parser.reaction.buffer_enhance_factors
    """
    # collider to lindemann
    fct_dct1 = chemkin_io.parser.reaction.buffer_enhance_factors(
        LINDEMANN_REACTION)
    fct_dct2 = chemkin_io.parser.reaction.buffer_enhance_factors(
        TROE_REACTION)
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
    print('\nPLog parameters')
    print(params1)
    print(params2)


def test__chebyshev_parameters():
    """ test chemkin_io.parser.reaction.chebyshev_parameters
    """
    params = chemkin_io.parser.reaction.chebyshev_parameters(
        CHEBYSHEV_REACTION)
    print('\nChebyshev parameters')
    print(params)


if __name__ == '__main__':
    test__data_strings()
    test__reactant_names()
    test__product_names()
    test__high_p_parameters()
    test__low_p_parameters()
    test__troe_parameters()
    test__buffer_enhance_factors()
    test__plog_parameters()
    test__chebyshev_parameters()
