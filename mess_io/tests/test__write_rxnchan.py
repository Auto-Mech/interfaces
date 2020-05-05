""" Tests the writing of the species section
"""

import mess_io


MOLECULE_MESS_STRING = """RRHO
  Core RigidRotor
    SymmetryFactor          1.0
  End
  Geometry[angstrom]        3
    O   1.911401284  0.16134481659  -0.05448080419
    N   4.435924209  0.16134481659  -0.05448080419
    N   6.537299661  0.16134481659  -0.05448080419
  Frequencies[1/cm]         9
    100.00  200.00  300.00  400.00  500.00
    600.00  700.00  800.00  900.00
  ElectronicLevels[1/cm]    2
    1  0.0
    3  50.0
"""

ATOM_MESS_STRING = """Atom
  Name O
  ElectronicLevels[1/cm]    3
    1  0.0
    3  150.0
    9  450.0
"""

ZERO_ENERGY = -35.0


def test__species_writer():
    """ Writes the MESS input for a Well
    """

    # Set a label for the well
    species_label = 'TEST'

    # Set the data string to the global molecule section
    species_data = MOLECULE_MESS_STRING

    # Use the writer to create a string for well section
    species_section_str = mess_io.writer.rxnchan.species(
        species_label, species_data, ZERO_ENERGY)

    # Print the well section string
    print('\n'+species_section_str)


def test__well_writer():
    """ Writes the MESS input for a Well
    """

    # Set a label for the well
    well_label = 'W1'

    # Set the data string to the global molecule section
    well_data = MOLECULE_MESS_STRING

    # Use the writer to create a string for well section
    well_section_str = mess_io.writer.rxnchan.well(
        well_label, well_data, ZERO_ENERGY)

    # Print the well section string
    print('\n'+well_section_str)


def test__bimolecular_writer():
    """ Writes the MESS input for a bimolecular set
    """

    # Set a label for the bimolecular set
    bimol_label = 'R1'

    # Set labels for the two species in the bimolecular set
    species1_label = 'Mol1'
    species2_label = 'Mol2'

    # Set the data strings to the global atom and molecule strings
    species1_data = ATOM_MESS_STRING
    species2_data = MOLECULE_MESS_STRING

    # Set the ground energy variable
    ground_energy = 50.0

    # Use the writer to create a string for the molecule section
    bimolecular_str = mess_io.writer.rxnchan.bimolecular(
        bimol_label,
        species1_label, species1_data,
        species2_label, species2_data,
        ground_energy)

    # Print the bimol section string
    print('\n'+bimolecular_str)


def test__ts_sadpt_writer():
    """ ts sadpt writer
    """

    # Set the data string to the global molecule section
    ts_data = MOLECULE_MESS_STRING

    # Set labels for TS
    ts_label = 'B1'
    reac_label = 'R1'
    prod_label = 'P1'

    tunnel_string = """Tunneling  Eckart
  ImaginaryFrequency[1/cm]  2000
  WellDepth[kcal/mol]       10
  WellDepth[kcal/mol]       20"""

    # Use the writer to create a string for the ts sadpt section
    ts_sadpt_str = mess_io.writer.rxnchan.ts_sadpt(
        ts_label, reac_label, prod_label, ts_data, ZERO_ENERGY,
        tunnel=tunnel_string)

    # Print the ts sadpoint section
    print('\n'+ts_sadpt_str)


def test__ts_variational_writer():
    """ ts mess_io.writer.rxnchan.ts_variational
    """

    # Set the number of points along the var
    nvar = 21

    # Loop over all the points of the var and build MESS strings
    var_pt_strings = []
    for i in range(nvar):
        var_pt_string = '+++++++++++++++++++++++++++++++++++'
        var_pt_string += '! IRC Point {0}\n'.format(str(i+1))
        var_pt_string += MOLECULE_MESS_STRING
        var_pt_strings.append(var_pt_string)

    # Set labels for TS
    ts_label = 'B1'
    reac_label = 'R1'
    prod_label = 'P1'

    tunnel_string = """Tunneling  Eckart
  ImaginaryFrequency[1/cm]  2000
  WellDepth[kcal/mol]       10
  WellDepth[kcal/mol]       20"""

    # Use the writer to create a string for the ts variational section
    ts_var_str = mess_io.writer.rxnchan.ts_variational(
        ts_label, reac_label, prod_label,
        var_pt_strings, tunnel=tunnel_string)

    # Print the ts sadpoint section
    print('\n'+ts_var_str)


if __name__ == '__main__':
    test__species_writer()
    test__well_writer()
    test__bimolecular_writer()
    test__ts_sadpt_writer()
    test__ts_variational_writer()
