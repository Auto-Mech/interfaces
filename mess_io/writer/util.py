"""
Utility functions
"""

import os
from mako.template import Template
import numpy
import autoparse.pattern as app
import autoparse.find as apf


# Build the MESS string using the mako template
def build_mako_str(template_file_name, template_src_path, template_keys):
    """ Using dct of keys and file paths, write the string with template
    """
    template_file_path = os.path.join(template_src_path, template_file_name)
    mess_str = Template(filename=template_file_path).render(**template_keys)

    return remove_trail_whitespace(mess_str)


# Format strings to have clean files
def indent(string, nspaces):
    """ Indents a multiline string. Required for Python 2,
        import textwrap textwrap.indent works for Python 3
    """
    pad = nspaces * ' '
    indented_string = ''.join(pad+line for line in string.splitlines(True))

    return indented_string


def remove_trail_whitespace(string):
    """ remove trailing spaces, and empty lines from a string
    """
    empty_line = app.LINE_START + app.maybe(app.LINESPACES) + app.NEWLINE
    trailing_spaces = app.LINESPACES + app.LINE_END
    pattern = app.one_of_these([empty_line, trailing_spaces])
    return apf.remove(pattern, string)


# Format various pieces of data into strings for MESS input files
def elec_levels_format(elec_levels):
    """ Helps format the elec levels
    """

    # Get the number of elec levles
    nlevels = len(elec_levels)

    # Build elec levels string
    elec_levels_string = ''
    for i, level in enumerate(elec_levels):
        elec_levels_string += '  '.join(map(str, level))
        if (i+1) != len(elec_levels):
            elec_levels_string += '\n'

    # Indent the lines
    elec_levels_string = indent(elec_levels_string, 4)

    return nlevels, elec_levels_string


def geom_format(geom):
    """ Helps format the geometry
    """

    # Get the number of atoms
    natoms = len(geom)

    # Build geom string; converting the coordinates to angstrom
    geom_string = ''
    for (asymb, xyz) in geom:
        geom_string += '{:<4s}{:>14.5f}{:>14.5f}{:>14.5f}\n'.format(
                        asymb, *tuple([val*0.529177 for val in xyz]))

    # Remove final newline character and indent the lines
    geom_string = indent(geom_string.rstrip(), 4)

    return natoms, geom_string


def freqs_format(freqs):
    """ Helps format the frequencies
    """

    # Get the number of freqs
    nfreqs = len(freqs)

    # Build freqs string
    freq_string = ''
    for i, freq in enumerate(freqs):
        if ((i+1) % 6) == 0 and (i+1) != len(freqs):
            freq_string += '{0:<8.0f}\n'.format(int(freq))
        else:
            freq_string += '{0:<8.0f}'.format(freq)

    # Indent the lines
    freq_string = indent(freq_string, 4)

    return nfreqs, freq_string


def format_rotor_key_defs(hind_rot_keyword_vals, remdummy=None):
    """ formats Group, Axis, Symmetry keywords
    """

    # Build string containing the values of each keyword
    hind_rot_keyword_string = ''
    for vals in hind_rot_keyword_vals:
        if remdummy is not None:
            hind_rot_keyword_string += '{0:<4d}'.format(
                int(vals - remdummy[vals-1]))
        else:
            hind_rot_keyword_string += '{0:<4d}'.format(vals)

    return hind_rot_keyword_string


def format_rotor_potential(potential):
    """ Helps format hindered rotor potential sections
    """

    # Get the number of the terms in the potential
    npotential = len(potential)

    # Build potentials string
    potential_string = ''
    for i, energy in enumerate(potential):
        if ((i+1) % 6) == 0 and (i+1) != npotential:
            potential_string += '{0:<8.2f}\n'.format(energy)
        else:
            potential_string += '{0:<8.2f}'.format(energy)

    # Indent the lines
    potential_string = indent(potential_string, 4)

    return npotential, potential_string


def format_rovib_coups(rovib_coups):
    """ Format the rovibrational couplings
    """

    # Join the values into a string
    rovib_coups_str = '  '.join(str(val) for val in rovib_coups)

    # Indent the lines
    rovib_coups_str = indent(rovib_coups_str, 4)

    return rovib_coups_str


def format_rot_dist_consts(rot_dists):
    """ Format the rotational distortion constants.
    """

    # Build rotational dists string
    rot_dists_string = ''
    for i, const in enumerate(rot_dists):
        rot_dists_string += '  '.join(map(str, const))
        if (i+1) != len(rot_dists):
            rot_dists_string += '\n'

    # Indent the lines
    rot_dists_string = indent(rot_dists_string, 4)

    return rot_dists_string


def format_xmat(xmat):
    """ Format the xmat anharm section
    """

    xmat = numpy.array(xmat)
    # Loop over the rows of the anharm numpy array
    anharm_string = ''
    for i in range(xmat.shape[0]):
        anharm_string += ' '.join(
            ['{0:>12.5f}'.format(val) for val in list(xmat[i, :i+1])
             if val != 0.0]
        )
        if (i+1) != xmat.shape[0]:
            anharm_string += '\n'

    # Indent the lines
    anharm_string = indent(anharm_string, 2)

    return anharm_string


def molec_spec_format(geom):
    """ Helps format the molecular section from the geometry
    """

    # Build geom string; converting the coordinates to angstrom
    atom_list_string = ''
    for (asymb, _) in geom:
        atom_list_string += '{:s} '.format(asymb)

    # Remove final newline character
    atom_list_string = atom_list_string.rstrip()

    # Indent the lines
    atom_list_string = indent(atom_list_string, 6)

    return atom_list_string


def format_flux_mode_indices(atom_indices):
    """ formats the atom indices for flux modes
    """

    # Build string containing the values of each keyword
    flux_mode_idx_string = ''
    for vals in atom_indices:
        flux_mode_idx_string += '{0:<4d}'.format(vals)

    return flux_mode_idx_string


# Helpful checker to set MESS string writing
def is_atom_in_str(species_data_str):
    """ searches for an atom in the str
    """
    return bool('Atom' in species_data_str)
