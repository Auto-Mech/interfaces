""" test chemkin_io.parser.thermo
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

SYNGAS_PATH = os.path.join(PATH, '../data/syngas')
SYNGAS_MECH_STR = _read_file(os.path.join(SYNGAS_PATH, 'mechanism.txt'))
SYNGAS_THERMO_BLOCK = chemkin_io.parser.util.clean_up_whitespace(
    chemkin_io.parser.mechanism.thermo_block(SYNGAS_MECH_STR))
SYNGAS_CSV_STR = _read_file(os.path.join(SYNGAS_PATH, 'smiles.csv'))

TEMP1 = 500.0
TEMP2 = 1000.0

# print('\n\nSpecies Polynomial from Mechanism File')
# print(SPECIES_POLYNOMIAL)


def test__species_name():
    """ test chemkin_io.parser.thermo.species_name
    """
    ref_name = 'S(1041)'
    name = chemkin_io.parser.thermo.species_name(
        SPECIES_POLYNOMIAL)
    assert name == ref_name


def test__temperatures():
    """ test chemkin_io.parser.thermo.temperatures
    """
    ref_temps = (100.0, 5000.0, 851.17)
    temps = chemkin_io.parser.thermo.temperatures(
        SPECIES_POLYNOMIAL)
    assert temps == ref_temps


def test__low_coefficients():
    """ test chemkin_io.parser.thermo.low_coefficients
    """
    ref_low_cfts = (1.38316741, 0.0607301618, -6.87644932e-05, 4.63273342e-08,
                    -1.30767374e-11, -27488.4597, 23.3435776)
    low_cfts = chemkin_io.parser.thermo.low_coefficients(
        SPECIES_POLYNOMIAL)
    assert low_cfts == ref_low_cfts


def test__high_coefficients():
    """ test chemkin_io.parser.thermo.high_coefficients
    """
    ref_high_cfts = (8.16250741, 0.0288724022, -1.26242468e-05, 2.35789979e-09,
                     -1.62798977e-13, -28642.576, -8.27062078)
    high_cfts = chemkin_io.parser.thermo.high_coefficients(
        SPECIES_POLYNOMIAL)
    assert high_cfts == ref_high_cfts


def test__data_block():
    """ test chemkin_io.parser.thermo.data_block
    """
    ref_block = ('S(1041)',
                 (100.0, 5000.0, 851.17),
                 (1.38316741, 0.0607301618, -6.87644932e-05, 4.63273342e-08,
                  -1.30767374e-11, -27488.4597, 23.3435776),
                 (8.16250741, 0.0288724022, -1.26242468e-05, 2.35789979e-09,
                  -1.62798977e-13, -28642.576, -8.27062078))
    block_str = chemkin_io.parser.thermo.data_block(
        NATGAS_THERMO_BLOCK)
    assert ref_block == block_str[SPECIES_IDX]


def test__data_strings():
    """ test chemkin_io.parser.thermo.data_strings
    """
    thm_strs = chemkin_io.parser.thermo.data_strings(
        NATGAS_THERMO_BLOCK)
    assert len(thm_strs) == 130


def test__dct_name_idx():
    """ test chemkin_io.parser.thermo.dct_name_idx
    """
    thm_dct = chemkin_io.parser.thermo.dct_name_idx(
        NATGAS_THERMO_BLOCK)
    for i, (key, val) in enumerate(thm_dct.items()):
        print('\n')
        print(key)
        print(val)
        if i == 20:
            break


def test__dct_inchi_idx():
    """ test chemkin_io.parser.thermo.dct_inchi_idx
    """
    name_inchi_dct = chemkin_io.parser.mechanism.species_inchi_dct(
        SYNGAS_CSV_STR)
    thm_dct = chemkin_io.parser.thermo.dct_inchi_idx(
        SYNGAS_THERMO_BLOCK, name_inchi_dct)
    for i, (key, val) in enumerate(thm_dct.items()):
        print('\n')
        print(key)
        print(val)
        if i == 20:
            break


def test__temp_common_default():
    """ test chemkin_io.parser.thermo.temp_common_default
    """
    ref_temp_common = 1000.0
    temp_common = chemkin_io.parser.thermo.temp_common_default(
        NATGAS_THERMO_BLOCK)
    assert ref_temp_common == temp_common


if __name__ == '__main__':
    test__species_name()
    test__temperatures()
    test__low_coefficients()
    test__high_coefficients()
    test__data_block()
    test__dct_name_idx()
    test__dct_inchi_idx()
    test__temp_common_default()
