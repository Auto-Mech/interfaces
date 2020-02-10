"""
  Tests the varecof_io.writer functions
"""

import varecof_io.writer

# For test__corr_potentials writer
NPOT = 5
BND_IDXS = [1, 3]
RVALS = [1.5958, 1.6958, 1.7958, 1.8958, 1.9958,
         2.0958, 2.1958, 2.2958, 2.3958, 2.4958]

POTENTIALS = [
    [0.052, 0.175, 0.430, 0.724, 0.996,
     1.199, 1.308, 1.317, 1.243, 1.113],
    [-0.722, -0.517, -0.372, -0.277, -0.218,
     -0.181, -0.153, -0.126, -0.096, -0.064],
    [0.224, 0.329, 0.556, 0.823, 1.071,
     1.255, 1.348, 1.346, 1.263, 1.127]
]
SPECIES_NAME = 'mol'
POT_LABELS = ['basis+relaxed', 'basis', 'relaxed']
FORTRAN_COMPILER = 'gfortran'
SPECIES_CORR_POTENTIALS = ['mol']
DIST_RESTRICT_IDXS = [[1, 5]]

# For test__compile_correction_potential
MAKE_PATH = '.'


def test__species_writer():
    """ tests varecof_io.writer.corr_potentials.species
    """

    # Write the species_corr.f string with no distance constraints
    species_corr_str = varecof_io.writer.corr_potentials.species(
        RVALS, POTENTIALS, BND_IDXS)
    with open('mol_corr.f', 'w') as mol_corr_file:
        mol_corr_file.write(species_corr_str)

    # Write the species_corr.f string with no distance constraints
    species_corr_str = varecof_io.writer.corr_potentials.species(
        RVALS, POTENTIALS, BND_IDXS,
        species_name=SPECIES_NAME, pot_labels=POT_LABELS)
    with open('mol_corr_wnames.f', 'w') as mol_corr_file:
        mol_corr_file.write(species_corr_str)

    # Write the species_corr.f string with no distance constraints
    species_corr_str = varecof_io.writer.corr_potentials.species(
        RVALS, POTENTIALS, BND_IDXS,
        dist_restrict_idxs=DIST_RESTRICT_IDXS)
    with open('mol_corr_constraint.f', 'w') as mol_corr_file:
        mol_corr_file.write(species_corr_str)


def test__dummy_writer():
    """ tests varecof_io.writer.corr_potentials.dummy
    """
    dummy_corr_str = varecof_io.writer.corr_potentials.dummy()
    with open('dummy_corr.f', 'w') as dummy_corr_file:
        dummy_corr_file.write(dummy_corr_str)


def test__auxiliary_writer():
    """ tests varecof_io.writer.corr_potentials.auxiliary
    """
    pot_aux_str = varecof_io.writer.corr_potentials.auxiliary()
    with open('pot_aux.f', 'w') as pot_aux_file:
        pot_aux_file.write(pot_aux_str)


def test__makefile_writer():
    """ tests varecof_io.writer.corr_potentials.makefile
    """
    makefile_str = varecof_io.writer.corr_potentials.makefile(
        FORTRAN_COMPILER, pot_file_names=SPECIES_CORR_POTENTIALS)
    with open('makefile', 'w') as makefile_file:
        makefile_file.write(makefile_str)


def test__compile_correction_potential():
    """ test varecof_io.writer.corr_potentials.compile_correction_pot
    """
    varecof_io.writer.corr_potentials.compile_corr_pot(
        MAKE_PATH)


if __name__ == '__main__':
    test__species_writer()
    test__dummy_writer()
    test__auxiliary_writer()
    test__makefile_writer()
    # test__compile_correction_potential()
