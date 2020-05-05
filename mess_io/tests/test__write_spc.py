""" Tests the writing of the energy transfer section
"""

import mess_io


def test__atom_writer():
    """ Writes a string containing all info for an atom in MESS style
    """

    # Set the name and electronic levels for the atom
    atom_mass = '16.0'
    atom_elec_levels = ((1, 0.00), (3, 150.0), (9, 450.0))

    # Use the writer to create a string for the atom section
    atom_section_str = mess_io.writer.species.atom(
        atom_mass, atom_elec_levels)

    # Print the atom section string
    print(atom_section_str)


def test__molecule_writer():
    """ Writes a string containing all info for a molecule in MESS style
    """

    # Set the information for a molecule
    mol_geom = (('O', (1.911401284, 0.16134481659, -0.05448080419)),
                ('N', (4.435924209, 0.16134481659, -0.05448080419)),
                ('N', (6.537299661, 0.16134481659, -0.05448080419)))
    mol_symfactor = 1.000
    mol_freqs = (100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0)
    mol_elec_levels = ((1, 0.0), (3, 50.0))
    interp_emax = ''

    # Get the string for the core using the geometry
    mol_core = mess_io.writer.mol_data.core_rigidrotor(
        mol_geom, mol_symfactor, interp_emax=interp_emax)

    # Use the writer to create a string for the molecule section
    molecule_section_str1 = mess_io.writer.species.molecule(
        mol_core, mol_freqs,
        mol_elec_levels,
        hind_rot='',
        rovib_coups='', rot_dists='')

    ## Set the additional optional keywords for
    hind_rot = """Rotor  Hindered
  Group                11  10  9   8   7   6
  Axis                 3   2   1
  Symmetry             1
  Potential[kcal/mol]  12
    0.00    2.91    9.06    12.63   9.97    3.51
    -0.03   3.49    9.96    12.63   9.08    2.93
End"""

    xmat = [[10000, 2000, 4000],
            [2000, 3000, 5000],
            [4000, 5000, 6000]]
    rovib_coups = [100, 200, 300]
    rot_dists = [['aaaa', 1000], ['bbaa', 2000], ['bbbb', 3000]]

    # Use the writer to create a string for the molecule section
    molecule_section_str2 = mess_io.writer.species.molecule(
        mol_core, mol_freqs,
        mol_elec_levels,
        hind_rot=hind_rot,
        xmat=xmat,
        rovib_coups=rovib_coups,
        rot_dists=rot_dists)

    # Print the molecule section string
    print(molecule_section_str1)
    print('\n')
    print(molecule_section_str2)


if __name__ == '__main__':
    test__atom_writer()
    test__molecule_writer()
