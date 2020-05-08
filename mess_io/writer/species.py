"""
Writes a section for an atom or molecule for the MESS input file.
Generally placed within a MESS "species", "well",
"bimolecular", or "barrier" section.

Takes in data from other MESS writer functions
"""

import os
from mako.template import Template
from mess_io.writer import util


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')
SPECIES_PATH = os.path.join(TEMPLATE_PATH, 'species')


def atom(mass, elec_levels):
    """ Writes the atom section of a MESS input file.
        :param int mass: mass of the atom (of desired isotope)
        :param list float elec_levels: energy and degeneracy of
                                       the atom's electronic states
        :return atom_str: String for the atom section
        :rtype: string
    """

    # Build a formatted elec levels string
    nlevels, levels = util.elec_levels_format(elec_levels)

    # Create dictionary to fill template
    atom_keys = {
        'mass': mass,
        'nlevels': nlevels,
        'levels': levels
    }

    return util.build_mako_str(
        template_file_name='atom.mako',
        template_src_path=SPECIES_PATH,
        template_keys=atom_keys)


def molecule(core, freqs, elec_levels,
             hind_rot='', xmat=(),
             rovib_coups=(), rot_dists=()):
    """ Writes the molecule section of a MESS input file
        :param str core: string for the "Core" section written
                         by another mess_io function
        :param list freqs: vibrational frequencies for the molecule
        :param list float elec_levels: energy and degeneracy of
                                       the molecule's electronic states
        :return atom_str: String for the atom section
        :rtype: string
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

    return util.build_mako_str(
        template_file_name='molecule.mako',
        template_src_path=SPECIES_PATH,
        template_keys=molec_keys)
