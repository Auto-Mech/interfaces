"""
compare thermo
"""

import os
from chemkin_io.calculator import combine


RC = 1.98720425864083e-3  # Gas Constant in kcal/mol.K


# Get mechanism information
def _read_file(file_name):
    with open(file_name, encoding='utf8', errors='ignore') as file_obj:
        file_str = file_obj.read()
    return file_str


PATH = os.path.dirname(os.path.realpath(__file__))

MECH1_PATH = os.path.join(PATH, '../data/syngas')
MECH1_STR = _read_file(os.path.join(
    MECH1_PATH, 'mechanism_green.txt'))
MECH1_CSV_STR = _read_file(os.path.join(
    MECH1_PATH, 'smiles_green.csv'))

MECH2_PATH = os.path.join(PATH, '../data/syngas')
MECH2_STR = _read_file(os.path.join(
    MECH2_PATH, 'mechanism_elte_2016_ijck.txt'))
MECH2_CSV_STR = _read_file(os.path.join(
    MECH2_PATH, 'smiles_elte_alt.csv'))

# Set index for the data dictionaries for the mechanisms
INDEX = 'inchi'

# Temperatures to run
# TEMPS = [500.0, 1000.0, 1500.0]
TEMPS = [300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0,
         1300.0, 1400.0, 1500.0, 1600.0, 1700.0, 1800.0, 1900.0, 2000.0,
         2300.0, 2400.0, 2500.0, 2600.0, 2700.0, 2800.0, 2900.0, 3000.0]


def test__compare_thermo():
    """ test chemkin_io.calculator.combine.mechanism_thermo
    """

    # Build dictionaries containing the thermo data strings for each species
    # Dictionaries indexed by the given mechanism names or InCHI string
    if INDEX == 'name':
        mech1_thermo_dct, mech2_thermo_dct = combine.build_thermo_name_dcts(
            MECH1_STR, MECH2_STR, TEMPS)
    elif INDEX == 'inchi':
        mech1_thermo_dct, mech2_thermo_dct = combine.build_thermo_inchi_dcts(
            MECH1_STR, MECH2_STR, MECH1_CSV_STR, MECH2_CSV_STR, TEMPS)

    print('\nMech1 thermo dct')
    for key, val in mech1_thermo_dct.items():
        print(key)
        print(val)
    print('\n\nMech2 thermo dct')
    for key, val in mech2_thermo_dct.items():
        print(key)
        print(val)

    # Calculate Enthalpy, Entropy, Gibbs, & Heat Capacity for each species
    # Mech 1 and 2 thermo data collated for each species
    thermo_vals_dct = combine.mechanism_thermo(
        mech1_thermo_dct, mech2_thermo_dct)

    print('\n\n\nCombined thermo vals')
    for idx in thermo_vals_dct:

        # # Obtain the name of each species to print for ID purposes
        # if INDEX == 'name':
        #     mech1_name = idx
        #     mech2_name = idx
        # elif INDEX == 'inchi':
        #     print('\n\nInChI: ', idx)
        #     mech1_name, mech2_name = combine.mech_name_from_inchi(
        #         MECH1_CSV_STR, MECH2_CSV_STR, idx)
        # print('M1 Name: ', mech1_name)
        # print('M2 Name: ', mech2_name)

        # Print all of the thermo quantities
        mech1_vals = thermo_vals_dct[idx]['mech1']
        mech2_vals = thermo_vals_dct[idx]['mech2']
        print('\nM1 Enthalpy', mech1_vals[0])
        print('M2 Enthalpy', mech2_vals[0])
        print('M1 Heat Capacity', mech1_vals[1])
        print('M2 Heat Capacity', mech2_vals[1])
        print('M1 Entropy', mech1_vals[2])
        print('M2 Entropy', mech2_vals[2])
        print('M1 Gibbs', mech1_vals[3])
        print('M2 Gibbs', mech2_vals[3])

    print('\n\n\n\n\n\n')
    print(thermo_vals_dct)


if __name__ == '__main__':
    test__compare_thermo()
