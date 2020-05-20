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
    """ Uses an input dictionary to fill in Mako template file containing the
        keys of the dictionary, then writes a string corresponding to the 
        filled-in Mako template.
        :param string template_file_name: Name of the Mako template file
        :param string template_src_path: Path where Mako template file resides
        :param dct template_keys: keys and values used to fill Mako template 
        :return mako_str: filled-in Mako template
        :rtype: string
    """
    template_file_path = os.path.join(template_src_path, template_file_name)
    mess_str = Template(filename=template_file_path).render(**template_keys)

    return remove_trail_whitespace(mess_str)


# Format strings to have clean files
def indent(string, nspaces):
    """ Indents each of the lines of a multiline string.
        :param string string: Input string to indent
        :param nspaces: number of spaces to indent the lines of the string
        :return indented_string: string indented by nspaces
        :rtype string
    """
    pad = nspaces * ' '
    indented_string = ''.join(pad+line for line in string.splitlines(True))

    return indented_string


def remove_trail_whitespace(string):
    """ Removes trailing spaces and empty lines from a input string.
        :param string string: Input string to clean up
        :return cleaned string
        :rtype: string
    """
    empty_line = app.LINE_START + app.maybe(app.LINESPACES) + app.NEWLINE
    trailing_spaces = app.LINESPACES + app.LINE_END
    pattern = app.one_of_these([empty_line, trailing_spaces])
    return apf.remove(pattern, string)


# Format various pieces of data into strings for MESS input files
def elec_levels_format(elec_levels):
    """ Formats the list of electronic energy levels into a string that
        is appropriate for a MESS input file.
        :param list elec_levels: levels of a species, given as 
                                 list-of-lists: [[energy, degeneracy], ...]
        :return elec_levels_str: MESS-format string containing levels
        :rtype string
    """

    # Get the number of elec levles
    nlevels = len(elec_levels)

    # Build elec levels string
    elec_levels_str = ''
    for i, level in enumerate(elec_levels):
        elec_levels_str += '  '.join(map(str, level))
        if (i+1) != len(elec_levels):
            elec_levels_str += '\n'

    # Indent the lines
    elec_levels_str = indent(elec_levels_str, 4)

    return nlevels, elec_levels_str


def geom_format(geom):
    """ Formats the geometry of a species into a string that
        is appropriate for a MESS input file.
        :param list geom: geometry
        :return natoms: number of atoms in the geometry
        :rtype int
        :return geom_string: MESS-format string containing geometry
        :rtype string
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
    """ Formats the vibrational frequencies of a species into a string that
        is appropriate for a MESS input file.
        :param list freqs: vibrational frequencies of species
        :return nfreqs: number of frequences for the species
        :rtype int
        :return freq_str: MESS-format string containing frequencies
        :rtype string
    """

    # Get the number of freqs
    nfreqs = len(freqs)

    # Build freqs string
    freq_str = ''
    for i, freq in enumerate(freqs):
        if ((i+1) % 6) == 0 and (i+1) != len(freqs):
            freq_str += '{0:<8.0f}\n'.format(int(freq))
        else:
            freq_str += '{0:<8.0f}'.format(freq)

    # Indent the lines
    freq_str = indent(freq_str, 4)

    return nfreqs, freq_str


def format_rotor_key_defs(rotor_keyword_vals, remdummy=None):
    """ Formats strings that contain the 'Group', 'Axis', and 'Symmetry'
        keywords and values that are used to define hindered rotors and
        internal rotors in MESS input files.
        :param list rotor_keyword_vals: values for the for some rotor keyword
        :param bool remdummy: idenitifies if a dummy atom requires val shift
        :return rotor_keyword_str: MESS-format string containing values
        :rtype string
    """

    # Build string containing the values of each keyword
    rotor_keyword_str = ''
    for vals in rotor_keyword_vals:
        if remdummy is not None:
            rotor_keyword_str += '{0:<4d}'.format(
                int(vals - remdummy[vals-1]))
        else:
            rotor_keyword_str += '{0:<4d}'.format(vals)

    return rotor_keyword_str


def format_rotor_potential(potential):
    """ Formats the potential energy surface along a rotor into a string
        used to define hindered rotors and internal rotors in MESS input files.
        :param list potential: values of potential along the rotor coordinate
        :param bool remdummy: idenitifies if a dummy atom requires val shift
        :return npotential: number of values in the potential
        :rtype int
        :return potential_str: values of potential in a MESS-format string
        :rtype string
    """

    # Get the number of the terms in the potential
    npotential = len(potential)

    # Build potentials string
    potential_str = ''
    for i, energy in enumerate(potential):
        if ((i+1) % 6) == 0 and (i+1) != npotential:
            potential_str += '{0:<8.2f}\n'.format(energy)
        else:
            potential_str += '{0:<8.2f}'.format(energy)

    # Indent the lines
    potential_str = indent(potential_str, 4)

    return npotential, potential_str


def format_rovib_coups(rovib_coups):
    """ Formats the matrix of rovibrational coupling terms for a species
        into a string appropriate for a MESS input file.
        :param numpy.ndarray rovib_coups: rovibrational coupling matrix
        :return rovib_coups_str: values of potential in a MESS-format string
        :rtype string
    """

    # Join the values into a string
    rovib_coups_str = '  '.join(str(val) for val in rovib_coups)

    # Indent the lines
    rovib_coups_str = indent(rovib_coups_str, 4)

    return rovib_coups_str


def format_rot_dist_consts(rot_dists):
    """ Formats the list of rotational distortion constants
        into a string appropriate for a MESS input file.
        :param list rot_dists: rotational distortion constants: 
                               [['aaa'], [val],...]
        :return rot_dists_str: values of potential in a MESS-format string
        :rtype string
    """
    """ Format the rotational distortion constants.
    """

    # Build rotational dists string
    rot_dists_str = ''
    for i, const in enumerate(rot_dists):
        rot_dists_str += '  '.join(map(str, const))
        if (i+1) != len(rot_dists):
            rot_dists_str += '\n'

    # Indent the lines
    rot_dists_str = indent(rot_dists_str, 4)

    return rot_dists_str


def format_xmat(xmat):
    """ Formats the anharmonicity (X) matrix for a species
        into a string appropriate for a MESS input file.
        :param list xmat: anharmonicity matrix
        :return xmat_str: anharmonicity matrix in a MESS-format string
        :rtype string
    """


    xmat = numpy.array(xmat)

    # Loop over the rows of the anharm numpy array
    xmat_str = ''
    for i in range(xmat.shape[0]):
        xmat_str += ' '.join(
            ['{0:>12.5f}'.format(val) for val in list(xmat[i, :i+1])
             if val != 0.0]
        )
        if (i+1) != xmat.shape[0]:
            xmat_str += '\n'

    # Indent the lines
    xmat_str = indent(xmat_str, 2)

    return xmat_str


def molec_spec_format(geom):
    """ Parses out the atom labels of a Cartesian geometry and  
        formats them into a string appropriate for definining 
        molecular species for Monte Carlo calculations in MESS. 
        :param list geom: geometry
        :return atom_lst_str
        :rtype: string
    """

    # Build geom string; converting the coordinates to angstrom
    atom_lst_str = ''
    for (asymb, _) in geom:
        atom_lst_str += '{:s} '.format(asymb)

    # Remove final newline character
    atom_lst_str = atom_lst_str.rstrip()

    # Indent the lines
    atom_lst_str = indent(atom_lst_str, 6)

    return atom_lst_str


def format_flux_mode_indices(atom_indices):
    """ Formates the atom indices into a string that is used
        to define the fluxional (torsional) modes of a
        molecular species for Monte Carlo calculations in MESS. 
        :return flux_mode_idx_str: formatted string of indices
        :rtype: string
    """

    # Build string containing the values of each keyword
    flux_mode_idx_str = ''
    for vals in atom_indices:
        flux_mode_idx_str += '{0:<4d}'.format(vals)

    return flux_mode_idx_str


# Helpful checker to set MESS string writing
def is_atom_in_str(spc_str):
    """ Checks a MESS-formatted species data string to see
        if the species is, or contains, an Atom definition.
        param: spc_str: MESS string containing species definitions
        return: is_atom_in_str
        rtype: bool
    """
    return bool('Atom' in spc_str)
