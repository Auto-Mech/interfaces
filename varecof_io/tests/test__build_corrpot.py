"""
  Tests the varecof_io.writer functions
"""

import os
import tempfile
import varecof_io


# Set paths for building files
PATH = tempfile.mkdtemp()
print(PATH)
DATA_PATH = os.path.join(PATH, 'data')
MOL_COR_PATH = os.path.join(PATH, 'mol_corr.f')
MOL_COR_WNAMES_PATH = os.path.join(PATH, 'mol_corr_wnames.f')
MOL_COR_CONST_PATH = os.path.join(PATH, 'mol_corr_constraint.f')
DUMMY_PATH = os.path.join(PATH, 'dummy_corr.f')
POT_AUX_PATH = os.path.join(PATH, 'pot_aux.f')
MAKEFILE_PATH = os.path.join(PATH, 'makefile')

# Set variables
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
FORTRAN_COMPILER = 'x86_64-conda_cos6-linux-gnu-gfortran'  # from conda-forge
SPECIES_CORR_POTENTIALS = ['mol']
DIST_RESTRICT_IDXS = [[1, 5]]


def test__species_writer():
    """ tests varecof_io.writer.corr_potentials.species
    """

    # Write the species_corr.f string with no distance constraints
    species_corr_str = varecof_io.writer.corr_potentials.species(
        RVALS, POTENTIALS, BND_IDXS)
    print(species_corr_str)

    # Write the species_corr.f string with no distance constraints
    species_corr_str = varecof_io.writer.corr_potentials.species(
        RVALS, POTENTIALS, BND_IDXS,
        species_name=SPECIES_NAME, pot_labels=POT_LABELS)
    print(species_corr_str)

    # Write the species_corr.f string with no distance constraints
    species_corr_str = varecof_io.writer.corr_potentials.species(
        RVALS, POTENTIALS, BND_IDXS,
        dist_restrict_idxs=DIST_RESTRICT_IDXS)
    print(species_corr_str)


def test__dummy_writer():
    """ tests varecof_io.writer.corr_potentials.dummy
    """
    dummy_corr_str = varecof_io.writer.corr_potentials.dummy()
    print(dummy_corr_str)


def test__auxiliary_writer():
    """ tests varecof_io.writer.corr_potentials.auxiliary
    """
    pot_aux_str = varecof_io.writer.corr_potentials.auxiliary()
    print(pot_aux_str)


def test__makefile_writer():
    """ tests varecof_io.writer.corr_potentials.makefile
    """
    makefile_str = varecof_io.writer.corr_potentials.makefile(
        FORTRAN_COMPILER, pot_file_names=SPECIES_CORR_POTENTIALS)
    print(makefile_str)


def test__compile_correction_potential():
    """ test varecof_io.writer.corr_potentials.compile_correction_pot
    """

    species_corr_str = varecof_io.writer.corr_potentials.species(
        RVALS, POTENTIALS, BND_IDXS)
    dummy_corr_str = varecof_io.writer.corr_potentials.dummy()
    pot_aux_str = varecof_io.writer.corr_potentials.auxiliary()
    makefile_str = varecof_io.writer.corr_potentials.makefile(
        FORTRAN_COMPILER, pot_file_names=SPECIES_CORR_POTENTIALS)

    with open(MOL_COR_PATH, 'w') as mol_corr_file:
        mol_corr_file.write(species_corr_str)
    with open(DUMMY_PATH, 'w') as dummy_corr_file:
        dummy_corr_file.write(dummy_corr_str)
    with open(POT_AUX_PATH, 'w') as pot_aux_file:
        pot_aux_file.write(pot_aux_str)
    with open(MAKEFILE_PATH, 'w') as makefile_file:
        makefile_file.write(makefile_str)

    varecof_io.writer.corr_potentials.compile_corr_pot(PATH)


if __name__ == '__main__':
    test__species_writer()
    test__dummy_writer()
    test__auxiliary_writer()
    test__makefile_writer()
    test__compile_correction_potential()
