"""
compare thermo
"""

import os
import numpy as np
from chemkin_io.calculator import combine


# Get mechanism information
def _read_file(file_name):
    with open(file_name, encoding='utf8', errors='ignore') as file_obj:
        file_str = file_obj.read()
    return file_str


PATH = os.path.dirname(os.path.realpath(__file__))
MECH1_PATH = os.path.join(PATH, '../data/test')
MECH1_STR = _read_file(os.path.join(MECH1_PATH, 'm1.txt'))
MECH1_CSV_STR = _read_file(os.path.join(MECH1_PATH, 'm1.csv'))
MECH2_PATH = os.path.join(PATH, '../data/test')
MECH2_STR = _read_file(os.path.join(MECH2_PATH, 'm2.txt'))
MECH2_CSV_STR = _read_file(os.path.join(MECH2_PATH, 'm2.csv'))

# Set index for the data dictionaries for the mechanisms
INDEX = 'inchi'

# Temperatures and Pressures to run
T_REF = 1.0
TEMPS = np.array([500.0, 1000.0, 1500.0])
# TEMPS = [300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0,
#          1300.0, 1400.0, 1500.0, 1600.0, 1700.0, 1800.0, 1900.0, 2000.0,
#          2300.0, 2400.0, 2500.0, 2600.0, 2700.0, 2800.0, 2900.0, 3000.0]
PRESSURES = np.array([1.0, 4.0, 5.0])


def test__compare_rates():
    """ test chemkin_io.mechparser.compare.rates
    """

    # Build dictionaries containing:
    # thermo data strings for each species, k data strings for each reaction
    # Dictionaries indexed by the given mechanism names or InCHI string
    if INDEX == 'name':
        _, mech2_thermo_dct = combine.build_thermo_name_dcts(
            MECH1_STR, MECH2_STR, TEMPS)
        mech1_ktp_dct, mech2_ktp_dct = combine.build_reaction_name_dcts(
            MECH1_STR, MECH2_STR,
            T_REF, TEMPS, PRESSURES)
    elif INDEX == 'inchi':
        _, mech2_thermo_dct = combine.build_thermo_inchi_dcts(
            MECH1_STR, MECH2_STR, MECH1_CSV_STR, MECH2_CSV_STR, TEMPS)
        mech1_ktp_dct, mech2_ktp_dct = combine.build_reaction_inchi_dcts(
            MECH1_STR, MECH2_STR, MECH1_CSV_STR, MECH2_CSV_STR,
            T_REF, TEMPS, PRESSURES)

    #print('\nMech1 reaction dct')
    for key, val in mech1_ktp_dct.items():
        print(key)
        print(val)
    #print('\n\nMech2 reaction dct')
    for key, val in mech2_ktp_dct.items():
        print(key)
        print(val)

    # Rate constant
    ktp_dct = combine.mechanism_rates(
        mech1_ktp_dct, mech2_ktp_dct,
        mech2_thermo_dct,
        TEMPS)

    # print dict
    print('\n\nktp dct')
    for rxn, mechs in ktp_dct.items():
        print(rxn)
        mech1, mech2 = mechs['mech1'], mechs['mech2']
        for (pr1, ktp1), (pr2, ktp2) in zip(mech1.items(), mech2.items()):
            print('Pressure: ', pr1, pr2)
            print('Mech1 ks: ', ktp1)
            print('Mech2 ks: ', ktp2)
            print(' ')


if __name__ == '__main__':
    test__compare_rates()
