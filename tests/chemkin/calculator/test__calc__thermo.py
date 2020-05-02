""" test chemkin_io.calculator.thermo
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
NATGAS_PATH = os.path.join(PATH, '../data/natgas')
NATGAS_MECH_STR = _read_file(os.path.join(NATGAS_PATH, 'mechanism.txt'))
NATGAS_THERMO_BLOCK = chemkin_io.parser.util.clean_up_whitespace(
    chemkin_io.parser.mechanism.thermo_block(NATGAS_MECH_STR))
NATGAS_BLOCK_STRS = chemkin_io.parser.thermo.data_strings(
    NATGAS_THERMO_BLOCK)
SPECIES_IDX = 100
SPECIES_POLYNOMIAL = NATGAS_BLOCK_STRS[SPECIES_IDX]

TEMP1 = 500.0
TEMP2 = 1000.0


def test__mechanism():
    """ test chemkin_io.calculator.thermo.mechanism
    """
    therm_dct = chemkin_io.calculator.thermo.mechanism(
        NATGAS_THERMO_BLOCK, [TEMP1, TEMP2])
    print(therm_dct)


def test__enthalpy():
    """ test chemkin_io.calculator.thermo.enthalpy
    """
    ref_ht1 = -42.58312043165988
    ref_ht2 = -19.266388540056756
    ht1 = chemkin_io.calculator.thermo.enthalpy(
        SPECIES_POLYNOMIAL, TEMP1)
    ht2 = chemkin_io.calculator.thermo.enthalpy(
        SPECIES_POLYNOMIAL, TEMP2)
    assert np.isclose(ref_ht1, ht1)
    assert np.isclose(ref_ht2, ht2)


def test__entropy():
    """ test chemkin_io.calculator.thermo.entropy
    """
    ref_st1 = 0.11016051269318868
    ref_st2 = 0.14192480698218363
    st1 = chemkin_io.calculator.thermo.entropy(
        SPECIES_POLYNOMIAL, TEMP1)
    st2 = chemkin_io.calculator.thermo.entropy(
        SPECIES_POLYNOMIAL, TEMP2)
    assert np.isclose(ref_st1, st1)
    assert np.isclose(ref_st2, st2)


def test__gibbs():
    """ test chemkin_io.calculator.thermo.gibbs
    """
    ref_gt1 = -97.66337677825422
    ref_gt2 = -161.1911955222404
    gt1 = chemkin_io.calculator.thermo.gibbs(
        SPECIES_POLYNOMIAL, TEMP1)
    gt2 = chemkin_io.calculator.thermo.gibbs(
        SPECIES_POLYNOMIAL, TEMP2)
    assert np.isclose(ref_gt1, gt1)
    assert np.isclose(ref_gt2, gt2)


def test__heat_capacity():
    """ test chemkin_io.calculator.thermo.heat_capacity
    """
    ref_cp1 = 0.038811581024503064
    ref_cp2 = 0.05285850615746261
    cp1 = chemkin_io.calculator.thermo.heat_capacity(
        SPECIES_POLYNOMIAL, TEMP1)
    cp2 = chemkin_io.calculator.thermo.heat_capacity(
        SPECIES_POLYNOMIAL, TEMP2)
    assert np.isclose(ref_cp1, cp1)
    assert np.isclose(ref_cp2, cp2)


if __name__ == '__main__':
    test__mechanism()
    test__enthalpy()
    test__entropy()
    test__gibbs()
    test__heat_capacity()
