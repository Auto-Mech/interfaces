"""
Writes a section for an atom or molecule for the MESS input file.
Generally placed within a MESS "species", "well",
"bimolecular", or "barrier" section.

Takes in data from other MESS writer functions
"""

import os
from ioformat import build_mako_str
from mess_io.writer import util


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')
SPECIES_PATH = os.path.join(TEMPLATE_PATH, 'species')


def atom(mass, elec_levels):
    """ Writes the string that defines the `Species` section
        for an atom for a MESS input file by
        formatting input information into strings and filling Mako template.

        :param mass: mass of the atom (of desired isotope)
        :type mass: int
        :param elec_levels: energy and degeneracy of atom's electronic states
        :type elec_levels: list(float)
        :rtype: str
    """

    # Build a formatted elec levels string
    nlevels, levels = util.elec_levels_format(elec_levels)

    # Create dictionary to fill template
    atom_keys = {
        'mass': mass,
        'nlevels': nlevels,
        'levels': levels
    }

    return build_mako_str(
        template_file_name='atom.mako',
        template_src_path=SPECIES_PATH,
        template_keys=atom_keys)


def molecule(core, freqs, elec_levels,
             hind_rot='', xmat=(),
             rovib_coups=(), rot_dists=()):
    """ Writes the string that defines the `Species` section
        for a molecule for a MESS input file by
        formatting input information into strings and filling Mako template.

        :param core: `Core` section string in MESS format
        :type core: str
        :param freqs: vibrational frequencies for the molecule
        :type freqs: list(float)
        :param elec_levels: energy and degeneracy of atom's electronic states
        :type elec_levels: list(float)
        ...
        :rtype: str
    """

    # Add in infrared intensities at some point

    # Build a formatted frequencies and elec levels string
    nfreqs, freqs = util.freqs_format(freqs)
    nlevels, levels = util.elec_levels_format(elec_levels)

    # Format the rovib couplings and rotational distortions if needed
    if rovib_coups:
        rovib_coups = util.format_rovib_coups(rovib_coups)
    else:
        rovib_coups = ''
    if rot_dists:
        rot_dists = util.format_rot_dist_consts(rot_dists)
    else:
        rot_dists = ''
    if xmat:
        anharm = util.format_xmat(xmat)
    else:
        anharm = ''

    # Indent various strings string if needed
    if hind_rot != '':
        hind_rot = util.indent(hind_rot, 2)

    # Create dictionary to fill template
    molec_keys = {
        'core': core,
        'nfreqs': nfreqs,
        'freqs': freqs,
        'nlevels': nlevels,
        'levels': levels,
        'hind_rot': hind_rot,
        'anharm': anharm,
        'rovib_coups': rovib_coups,
        'rot_dists': rot_dists,
    }

    return build_mako_str(
        template_file_name='molecule.mako',
        template_src_path=SPECIES_PATH,
        template_keys=molec_keys)
