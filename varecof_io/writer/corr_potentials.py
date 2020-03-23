"""
Writes the fortran files needed for the correction potential
"""

import os
import subprocess
from mako.template import Template
from varecof_io.writer import util


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')


def species(rvalues, potentials, bnd_frm_idxs,
            dist_restrict_idxs=(), pot_labels=(), species_name='mol'):
    """ Writes string for correction potential for some species Fortran file
        :return : String for the mol_corr.f file
        :rtype: string
    """

    npot = len(potentials)
    npot_terms = len(potentials[0])
    [aidx, bidx] = bnd_frm_idxs
    asym, bsym = 'A', 'B'

    assert npot > 0
    assert all(len(potential) == npot_terms for potential in potentials)

    # Put some comment lines giving a description of the correction potentials
    pot_labels_str = ''
    if pot_labels:
        for i, label in enumerate(pot_labels):
            pot_labels_str += 'c     dv{0} = {1} correction\n'.format(
                str(i+1), label)
    pot_labels_str = pot_labels_str.rstrip()

    # Strings to initialize the potential variables in the Fortran subroutine
    npot = len(potentials)
    npot_terms = len(potentials[0])
    dv_defs = ''
    for i in range(npot):
        dv_defs += 'dv{0}({1}),'.format(str(i+1), npot_terms)
    dv_defs = dv_defs[:-1]

    # Definitions of all of all the correction potential distances
    rvals = ''
    for i, rval in enumerate(rvalues):
        rvals += '      data rinp({0}) / {1:.3f} /\n'.format(
            str(i+1), rval)
    rvals = rvals.rstrip()
    rmin = min(rvalues)
    rmax = max(rvalues)

    # Definitions of all of all the correction potential energies
    dv_vals = ''
    for i, potential in enumerate(potentials):
        for j, term in enumerate(potential):
            dv_vals += '      data dv{0}({1}) / {2:.3f} /\n'.format(
                str(i+1), str(j+1), term)
    dv_vals = dv_vals.rstrip()

    # Build principal distance string
    bond_distance_string = util.format_corrpot_dist_string(
        aidx, bidx, asym, bsym)

    # Build distance restriction strings
    restrict_distance_strings = ''
    for i, idxs in enumerate(dist_restrict_idxs):
        [idx1, idx2] = idxs
        sym1, sym2 = chr(67+2*i), chr(68+2*i)
        restrict_distance_strings += util.format_corrpot_dist_string(
            idx1, idx2, sym1, sym2)
        restrict_distance_strings += '\n'
        restrict_distance_strings += util.format_restrict_dist_string(
            sym1, sym2, species_name)
        restrict_distance_strings += '\n'

    # Build the delmlt string
    delmlt_string = util.format_delmlt_string(asym, bsym)

    # Build the spline fitting strings
    spline_strings = util.format_spline_strings(npot, asym, bsym, species_name)

    # Create dictionary to fill template
    corr_keys = {
        'species_name': species_name,
        'pot_labels': pot_labels_str,
        'npot': npot,
        'npot_terms': npot_terms,
        'dv_defs': dv_defs,
        'rvals': rvals,
        'dv_vals': dv_vals,
        'rmin': rmin,
        'rmax': rmax,
        # 'aidx': aidx,
        # 'bidx': bidx,
        'bond_distance_string': bond_distance_string,
        'restrict_distance_strings': restrict_distance_strings,
        'delmlt_string': delmlt_string,
        'spline_strings': spline_strings
    }

    # Set template name and path for the species_corr template
    template_file_name = 'species_corr.mako'
    template_file_path = os.path.join(TEMPLATE_PATH, template_file_name)

    # Build species_corr.f string
    spc_corr_str = Template(filename=template_file_path).render(**corr_keys)

    return spc_corr_str


def dummy():
    """ Writes string for the dummy correction potention potential Fortran file
        :return : String for the dummy_corr.f file
        :rtype: string
    """

    # Set template name and path for the dummy_corr template
    template_file_name = 'dummy_corr.mako'
    template_file_path = os.path.join(TEMPLATE_PATH, template_file_name)

    # Build dummy_corr.f string
    dummy_corr_str = Template(filename=template_file_path).render()

    return dummy_corr_str


def auxiliary():
    """ Writes string for the potential auxiliary functions Fortran file
        :return : String for the pot_aux.f file
        :rtype: string
    """

    # Set template name and path for the pot_aux template
    template_file_name = 'pot_aux.mako'
    template_file_path = os.path.join(TEMPLATE_PATH, template_file_name)

    # Build pot_aux.f string
    pot_aux_str = Template(filename=template_file_path).render()

    return pot_aux_str


def makefile(fortran_compiler, pot_file_names=()):
    """ Writes string for a makefile to compile correction potentials
        :return : String for the makefile
        :rtype: string
    """

    # Set species name
    corr_potential_names = ''
    if pot_file_names:
        for potential in pot_file_names:
            corr_potential_names += '{0}_corr.f '.format(potential)

    make_keys = {
        'fc': fortran_compiler,
        'corr_potential_names': corr_potential_names
    }

    # Set template name and path for the pot_aux template
    template_file_name = 'makefile.mako'
    template_file_path = os.path.join(TEMPLATE_PATH, template_file_name)

    # Build pot_aux.f string
    makefile_str = Template(filename=template_file_path).render(**make_keys)

    return makefile_str


def compile_corr_pot(make_path):
    """ compile the correction potential
        :param str make_path: path to the makefile and correction potential src
    """
    subprocess.check_call(
        ['make'], cwd=make_path,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
