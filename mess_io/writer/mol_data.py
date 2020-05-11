"""
Writes MESS input for a molecule
"""

import os
import numpy
from mess_io.writer import util


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')
SPECIES_PATH = os.path.join(TEMPLATE_PATH, 'species')
SPEC_INFO_PATH = os.path.join(SPECIES_PATH, 'info')


def core_rigidrotor(geom, sym_factor, interp_emax=None):
    """ Writes a rigid-rotor core section.
    """

    # Format the geometry section
    natom, geom = util.geom_format(geom)

    # Create dictionary to fill template
    core_keys = {
        'sym_factor': sym_factor,
        'natom': natom,
        'geom': geom,
        'interp_emax': interp_emax
    }

    return util.build_mako_str(
        template_file_name='core_rigidrotor.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=core_keys)


def core_multirotor(geom, sym_factor, pot_surf, int_rot_str,
                    interp_emax=100, quant_lvl_emax=9):
    """ Writes a multi-rotor core section.
    """

    # Format the geometry section
    natom, geom = util.geom_format(geom)

    # Indent the internal rotor string
    int_rot_str = util.indent(int_rot_str, 2)

    # Create dictionary to fill template
    core_keys = {
        'sym_factor': sym_factor,
        'natom': natom,
        'geom': geom,
        'pot_surf': pot_surf,
        'int_rot': int_rot_str,
        'interp_emax': interp_emax,
        'quant_lvl_emax': quant_lvl_emax
    }

    return util.build_mako_str(
        template_file_name='core_multirotor.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=core_keys)


def core_phasespace(geom1, geom2, sym_factor, stoich,
                    pot_prefactor=10, pot_power_exp=6):
    """ Writes a core section for phase space theory
    """

    # Format the geometry section of each fragment
    natom1, geom1 = util.geom_format(geom1)
    natom2, geom2 = util.geom_format(geom2)

    # Indent the geometry strings
    geom1 = util.indent(geom1, 2)
    geom2 = util.indent(geom2, 2)

    # Create dictionary to fill template
    core_keys = {
        'sym_factor': sym_factor,
        'natom1': natom1,
        'geom1': geom1,
        'natom2': natom2,
        'geom2': geom2,
        'stoich': stoich,
        'pot_prefactor': pot_prefactor,
        'pot_power_exp': pot_power_exp
    }

    return util.build_mako_str(
        template_file_name='core_phasespace.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=core_keys)


def core_rotd(sym_factor, flux_file_name, stoich):
    """ Writes a core section which calls flux files from Rotd/VaReCoF
    """

    # Set values and template based on core type
    core_keys = {
        'sym_factor': sym_factor,
        'flux_file_name': flux_file_name,
        'stoich': stoich
    }

    return util.build_mako_str(
        template_file_name='core_rotd.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=core_keys)


def rotor_hindered(group, axis, symmetry, potential,
                   remdummy=None, geom=None, use_quantum_weight=False):
    """ Writes the section for a single hindered rotor.
    """
    # Format the sections
    rotor_group = util.format_rotor_key_defs(group, remdummy)
    rotor_axis = util.format_rotor_key_defs(axis, remdummy)
    rotor_npotential, rotor_potential = util.format_rotor_potential(potential)

    # Format the geom
    natom = 1
    if geom is not None:
        natom, geom = util.geom_format(geom)
        geom = util.indent(geom, 4)

    # Create dictionary to fill template
    rotor_keys = {
        'group': rotor_group,
        'axis': rotor_axis,
        'symmetry': symmetry,
        'npotential': rotor_npotential,
        'potential': rotor_potential,
        'natom': natom,
        'geom': geom,
        'use_quantum_weight': use_quantum_weight
    }

    return util.build_mako_str(
        template_file_name='rotor_hindered.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=rotor_keys)


def mdhr_data(potentials, freqs=()):
    """ Write a file containing the hindered rotor potentials
        Only writes the file for up to 4-dimensinal rotor
    """

    # Determine the dimensions of the rotor potential list
    dims = numpy.array(potentials).shape
    ndims = len(dims)

    # Write top line string with number of points in potential
    if ndims == 1:
        dat_str = '{0:>6d}'.format(*dims)
        nfreqs = len(freqs[0]) if freqs else None
    elif ndims == 2:
        dat_str = '{0:>6d}{1:>6d}'.format(*dims)
        nfreqs = len(freqs[0][0]) if freqs else None
    elif ndims == 3:
        dat_str = '{0:>6d}{1:>6d}{2:>6d}'.format(*dims)
        nfreqs = len(freqs[0][0][0]) if freqs else None
    elif ndims == 4:
        dat_str = '{0:>6d}{1:>6d}{2:>6d}{3:>6d}'.format(*dims)
        nfreqs = len(freqs[0][0][0][0]) if freqs else None

    # Add the nofreq line
    if freqs:
        dat_str += '\n '
        dat_str += ' '.join('{0:d}'.format(idx+1) for idx in range(nfreqs))
        dat_str += '\n\n'
    else:
        dat_str += '\n nofreq\n\n'

    # Write the strings with the potential values
    if ndims == 1:
        for i in range(dims[0]):
            dat_str += (
                '{0:>6d}{1:>15.8f}'.format(
                    i+1, potentials[i])
                )
            if freqs:
                ' {}'.join((freq for freq in freqs[i]))
            dat_str += '\n'
    elif ndims == 2:
        for i in range(dims[0]):
            for j in range(dims[1]):
                dat_str += (
                    '{0:>6d}{1:>6d}{2:>15.8f}'.format(
                        i+1, j+1, potentials[i][j])
                )
                if freqs:
                    strs = ('{0:d}'.format(int(val)) for val in freqs[i][j])
                    dat_str += '  ' + ' '.join(strs)
                dat_str += '\n'
    elif ndims == 3:
        for i in range(dims[0]):
            for j in range(dims[1]):
                for k in range(dims[2]):
                    dat_str += (
                        '{0:>6d}{1:>6d}{2:>6d}{3:>15.8f}'.format(
                            i+1, j+1, k+1, potentials[i][j][k])
                    )
                    if freqs:
                        ' {}'.join((freq for freq in freqs[i][j][k]))
                    dat_str += '\n'
    elif ndims == 4:
        for i in range(dims[0]):
            for j in range(dims[1]):
                for k in range(dims[2]):
                    for lma in range(dims[3]):
                        dat_str += (
                            '{0:>6d}{1:>6d}{2:>6d}{3:>6d}{4:>15.8f}'.format(
                                i+1, j+1, k+1, lma+1,
                                potentials[i][j][k][lma])
                        )
                        if freqs:
                            ' {}'.join((freq for freq in freqs[i][j][k][lma]))
                        dat_str += '\n'

    return util.remove_trail_whitespace(dat_str)


def rotor_internal(group, axis, symmetry,
                   rotor_id='', remdummy=None, geom=None,
                   mass_exp_size=5, pot_exp_size=5,
                   hmin=13, hmax=101,
                   grid_size=100):
    """ Writes the section for a single internal rotor.
    """

    # Format the sections
    rotor_group = util.format_rotor_key_defs(group, remdummy)
    rotor_axis = util.format_rotor_key_defs(axis, remdummy)

    # Format the geom
    if geom is not None:
        natom, geom = util.geom_format(geom)
        geom = util.indent(geom, 4)
    else:
        natom = None

    # Create dictionary to fill template
    rotor_keys = {
        'group': rotor_group,
        'axis': rotor_axis,
        'rotor_id': rotor_id,
        'symmetry': symmetry,
        'mass_exp_size': mass_exp_size,
        'pot_exp_size': pot_exp_size,
        'hmin': hmin,
        'hmax': hmax,
        'grid_size': grid_size,
        'natom': natom,
        'geom': geom
    }

    return util.build_mako_str(
        template_file_name='rotor_internal.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=rotor_keys)


def umbrella_mode(group, plane, ref_atom, potential,
                  remdummy=None, geom=None):
    """ Writes the section for a single hindered rotor.
    """
    # Format the sections
    umbr_group = util.format_rotor_key_defs(group, remdummy)
    umbr_plane = util.format_rotor_key_defs(plane, remdummy)
    umbr_npotential, umbr_potential = util.format_rotor_potential(potential)

    # Format the geom
    if geom is not None:
        natom, geom = util.geom_format(geom)
        geom = util.indent(geom, 4)
    else:
        natom = None

    # Create dictionary to fill template
    umbr_keys = {
        'group': umbr_group,
        'axis': umbr_plane,
        'ref_atom': ref_atom,
        'npotential': umbr_npotential,
        'potential': umbr_potential,
        'natom': natom,
        'geom': geom,
    }

    return util.build_mako_str(
        template_file_name='umbrella_mode.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=umbr_keys)


def tunnel_eckart(imag_freq, well_depth1, well_depth2):
    """ Writes the tunneling section assuming an Eckart model
    """
    # Format the imaginary frequency and well-depth values
    imag_freq = '{0:<8.0f}'.format(imag_freq)
    well_depth1 = '{0:<8.2f}'.format(well_depth1)
    well_depth2 = '{0:<8.2f}'.format(well_depth2)

    # Create dictionary to fill template
    tunnel_keys = {
        'imag_freq': imag_freq,
        'well_depth1': well_depth1,
        'well_depth2': well_depth2
    }

    return util.build_mako_str(
        template_file_name='tunnel_eckart.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=tunnel_keys)


def tunnel_sct(imag_freq, tunnel_file, cutoff_energy=2500):
    """ Writes the tunneling section accounting for small curvature tunneling
    """

    # Format the imaginary frequency value
    imag_freq = '{0:<8.0f}'.format(imag_freq)

    # Create dictionary to fill template
    tunnel_keys = {
        'imag_freq': imag_freq,
        'cutoff_energy': cutoff_energy,
        'tunnel_file': tunnel_file
    }

    return util.build_mako_str(
        template_file_name='tunnel_sct.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=tunnel_keys)
