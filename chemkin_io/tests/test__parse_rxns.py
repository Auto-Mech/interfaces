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


PATH = os.path.dirname(os.path.realpath(__file__))
SYNGAS_PATH = os.path.join(PATH, '../data/syngas')
SYNGAS_MECH_STR = _read_file(os.path.join(SYNGAS_PATH, 'mechanism.txt'))

SYNGAS_REACTION_BLOCK = chemkin_io.parser.util.clean_up_whitespace(
    chemkin_io.parser.mechanism.reaction_block(SYNGAS_MECH_STR))
SYNGAS_REACTION_STRS = chemkin_io.parser.reaction.data_strings(
    SYNGAS_REACTION_BLOCK)
REACTION = SYNGAS_REACTION_STRS[20]

TEST_PATH = os.path.join(PATH, '../data/syngas')
TEST_MECH_STR = _read_file(os.path.join(TEST_PATH, 'mechanism.txt'))

TEST_REACTION_BLOCK = chemkin_io.parser.util.clean_up_whitespace(
    chemkin_io.parser.mechanism.reaction_block(TEST_MECH_STR))
TEST_REACTION_STRS = chemkin_io.parser.reaction.data_strings(
    TEST_REACTION_BLOCK)
TEST_REACTION = TEST_REACTION_STRS[0]

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
    "C2H3+O2<=>C2H3OO  8.07E+27    -2.67   23222\n"
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
# print('\n\nRate Data for a Reaction')
# print(REACTION)

# print('\nhigh p')
# print(HIGHP_REACTION)
# print('\nlindemann')
# print(LINDEMANN_REACTION)
# print('\ntroe')
# print(TROE_REACTION)
# print('\nchebyshev')
# print(CHEBYSHEV_REACTION)
# print('\nplog')
# print(PLOG_REACTION)


def test__reactant_names():
    """ test chemkin_io.parser.reaction.reactant_names
    """
    names = chemkin_io.parser.reaction.reactant_names(
        TEST_REACTION)
    print('\nreactants')
    print(names)


def test__product_names():
    """ test chemkin_io.parser.reaction.product_names
    """
    names = chemkin_io.parser.reaction.product_names(
        TEST_REACTION)
    print('\nproducts')
    print(names)


def test__high_p_parameters():
    """ test chemkin_io.parser.reaction.high_p_parameters
    """
    params = chemkin_io.parser.reaction.high_p_parameters(
        LINDEMANN_REACTION)
    print('\nhigh-pressure parameters')
    print(params)


def test__low_p_parameters():
    """ test chemkin_io.parser.reaction.low_p_parameters
    """
    params = chemkin_io.parser.reaction.low_p_parameters(
        LINDEMANN_REACTION)
    print('\nlow-pressure parameters')
    print(params)


def test__troe_parameters():
    """ test chemkin_io.parser.reaction.troe_parameters
    """
    params = chemkin_io.parser.reaction.troe_parameters(
        TROE_REACTION)
    print('\nTroe parameters')
    print(params)


def test__chebyshev_parameters():
    """ test chemkin_io.parser.reaction.chebyshev_parameters
    """
    params = chemkin_io.parser.reaction.chebyshev_parameters(
        CHEBYSHEV_REACTION)
    print('\nChebyshev parameters')
    print(params)


def test__plog_parameters():
    """ test chemkin_io.parser.reaction.plog_parameters
    """
    params = chemkin_io.parser.reaction.plog_parameters(
        PLOG_REACTION)
    print('\nPLog parameters')
    print(params)


def test__buffer_enhance_factors():
    """ test chemkin_io.parser.reaction.buffer_enhance_factors
    """
    fct_dct = chemkin_io.parser.reaction.buffer_enhance_factors(
        LINDEMANN_REACTION)
    print('\nLow Pressure Buffer Enhhancement Factors')
    print(fct_dct)


def test__data_strings():
    """ test chemkin_io.parser.reaction.data_strings
    """

    rxn_strs = chemkin_io.parser.reaction.data_strings(
        TEST_REACTION_BLOCK)
    assert len(rxn_strs) == 1678


def test__duplicate_high_p_parameters():
    """ test chemkin_io.parser.reaction.high_p_parameters
    """
    params = chemkin_io.parser.reaction.high_p_parameters(
        DUP_HIGHP_REACTION)
    print('\nhigh-pressure parameters')
    print(params)


def test__duplicate_plog_parameters():
    """ test chemkin_io.parser.reaction.plog_parameters
    """
    params = chemkin_io.parser.reaction.plog_parameters(
        DUP_PLOG_REACTION)
    print('\nPLog parameters')
    for key, val in params.items():
        print(key)
        print(val)


if __name__ == '__main__':
    # test__reactant_names()
    # test__product_names()
    # test__high_p_parameters()
    test__duplicate_high_p_parameters()
    # test__low_p_parameters()
    # test__troe_parameters()
    # test__chebyshev_parameters()
    # test__plog_parameters()
    # test__buffer_enhance_factors()
    # test__data_strings()
    # test__duplicate_high_p_parameters()
    # test__duplicate_plog_parameters()
