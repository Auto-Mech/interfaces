"""
Writes MESS input for a molecule
"""

import os
import numpy
from ioformat import build_mako_str
from ioformat import indent
from ioformat import remove_trail_whitespace
from mess_io.writer import util


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')
SPECIES_PATH = os.path.join(TEMPLATE_PATH, 'species')
SPEC_INFO_PATH = os.path.join(SPECIES_PATH, 'info')


def core_rigidrotor(geom, sym_factor, interp_emax=None):
    """ Writes the string that defines the 'Core' section for a
        rigid-rotor model of a species for a MESS input file by
        formatting input information into strings a filling Mako template.

        :param geom: geometry of species
        :type geom: list
        :param sym_factor: symmetry factor of species
        :type sym_factor: float
        :param interp_emax: max energy to calculate num. of states (kcal.mol-1)
        :type interp_emax: float
        :rtype: str
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

    return build_mako_str(
        template_file_name='core_rigidrotor.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=core_keys)


def core_multirotor(geom, sym_factor, pot_surf_file, int_rot_str,
                    interp_emax=100, quant_lvl_emax=9):
    """ Writes the string that defines the `Core` section for a
        multidimensional rotor model of a species for a MESS input file by
        formatting input information into strings a filling Mako template.

        :param geom: geometry of species
        :type geom: list
        :param sym_factor: symmetry factor of species
        :type sym_factor: float
        :param pot_surf_file: name of file with PES along rotor (kcal.mol-1)
        :type pot_sur_file: str
        :param int_rot_str: MESS-format strings that define internal rotors
        :type int_rot_str: str
        :param interp_emax: max energy to calculate density/number of states
        :type interp_emax: float
        :param quant_lvl_emax: max energy to calculate quantum energy levels
        :type quant_lvl_emax: float
        :rtype: str
    """

    # Format the geometry section
    natom, geom = util.geom_format(geom)

    # Indent the internal rotor string
    int_rot_str = indent(int_rot_str, 2)

    # Create dictionary to fill template
    core_keys = {
        'sym_factor': sym_factor,
        'natom': natom,
        'geom': geom,
        'pot_surf_file': pot_surf_file,
        'int_rot': int_rot_str,
        'interp_emax': interp_emax,
        'quant_lvl_emax': quant_lvl_emax
    }

    return build_mako_str(
        template_file_name='core_multirotor.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=core_keys)


def core_phasespace(geom1, geom2, sym_factor, stoich,
                    pot_prefactor=10.0, pot_exp=6.0):
    """ Writes the string that defines the `Core` section for a
        phase space theory model of a transition state for a MESS input file by
        formatting input information into strings a filling Mako template.

        :param geom1: geometry of the dissociation species 1
        :type geom1: list
        :param geom2: geometry of the dissociation species 2
        :type geom2: list
        :param sym_factor: symmetry factor of transition state
        :type sym_factor: float
        :param stoich: combined stoichiometry of dissociation species 1 and 2
        :type stoich: str
        :param pot_prefator: factor C0 in potential expression V = -C0/R^n (au)
        :type pot_prefactor: float
        :param pot_power: power n in potential expression V = -C0/R^n (au)
        :type pot_power: float
        :rtype: str
    """

    # Format the geometry section of each fragment
    natom1, geom1 = util.geom_format(geom1)
    natom2, geom2 = util.geom_format(geom2)

    # Indent the geometry strings
    geom1 = indent(geom1, 2)
    geom2 = indent(geom2, 2)

    # Create dictionary to fill template
    core_keys = {
        'sym_factor': sym_factor,
        'natom1': natom1,
        'geom1': geom1,
        'natom2': natom2,
        'geom2': geom2,
        'stoich': stoich,
        'pot_prefactor': pot_prefactor,
        'pot_exp': pot_exp
    }

    return build_mako_str(
        template_file_name='core_phasespace.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=core_keys)


def core_rotd(sym_factor, flux_file_name, stoich):
    """ Writes the string that defines the `Core` section for a
        variational reaction-coordinate transition-state theory model of a
        transition state for a MESS input file by
        formatting input information into strings a filling Mako template.

        :param sym_factor: symmetry factor of transition state
        :type sym_factor: float
        :param flux_file_name:
        :type flux_file_name: str
        :param stoich: combined stoichiometry of dissociation species 1 and 2
        :type stoich: str
        :rtype: str
    """

    # Create dictionary to fill template
    core_keys = {
        'sym_factor': sym_factor,
        'flux_file_name': flux_file_name,
        'stoich': stoich
    }

    return build_mako_str(
        template_file_name='core_rotd.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=core_keys)


def rotor_hindered(group, axis, symmetry, potential,
                   remdummy=None, geom=None, use_quantum_weight=False):
    """ Writes the string that defines the `Rotor` section for a
        single hindered rotor of a species for a MESS input file by
        formatting input information into strings a filling Mako template.

        :param group: idxs for the atoms of one of the rotational groups
        :type group: list(int)
        :param axis: idxs for the atoms that make up the rotational axis
        :type axis: list(int)
        :param symmetry: overall symmetry of the torsional motion (potential)
        :type symmetry: int
        :param potential: value of the potential along torsion (kcal.mol-1)
        :type potential: list(float)
        :param remdummy: list of idxs of dummy atoms for shifting values
        :type remdummy: list(int)
        :param stoich: combined stoichiometry of dissociation species 1 and 2
        :type stoich: str
        :rtype: str
    """

    # Format the rotor sections
    rotor_group = util.format_rotor_key_defs(group, remdummy)
    rotor_axis = util.format_rotor_key_defs(axis, remdummy)
    rotor_npotential, rotor_potential = util.format_rotor_potential(potential)

    # Format the geom
    natom = 1
    if geom is not None:
        natom, geom = util.geom_format(geom)
        geom = indent(geom, 4)

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

    return build_mako_str(
        template_file_name='rotor_hindered.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=rotor_keys)


def rotor_internal(group, axis, symmetry, grid_size, mass_exp_size,
                   pot_exp_size=5, hmin=13, hmax=101,
                   rotor_id='', remdummy=None, geom=None):
    """ Writes the string that defines the `Rotor` section for a
        single internal rotor of a species for a MESS input file by
        formatting input information into strings a filling Mako template.

        :param group: idxs for the atoms of one of the rotational groups
        :type group: list(int)
        :param axis: idxs for the atoms that make up the rotational axis
        :type axis: list(int)
        :param symmetry: overall symmetry of the torsional motion (potential)
        :type symmetry: int
        :param grid_size: grid_size for statistical weight calculation
        :type grid_size: int
        :param mass_exp_size: num. mass expansion Fourier harmonics
        :type mass_exp_size: int
        :param pot_exp_size: num. potential expansion Fourier harmonics
        :type pot_exp_size: int
        :param hmin: minimum value for quantum phase space dimension
        :type hmin: int
        :param hmax: maximum value for quantum phase space dimension
        :type hmax: int
        :param remdummy: list of idxs of dummy atoms for shifting values
        :type remdummy: list(int)
        :param geom: geometry of the species the rotor exists for
        :type geom: list
        :rtype: str
    """

    assert mass_exp_size > 0 and mass_exp_size % 2 == 1
    assert pot_exp_size > 0 and pot_exp_size % 2 == 1

    # Format the sections
    rotor_group = util.format_rotor_key_defs(group, remdummy)
    rotor_axis = util.format_rotor_key_defs(axis, remdummy)

    # Format the geom
    if geom is not None:
        natom, geom = util.geom_format(geom)
        geom = indent(geom, 4)
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

    return build_mako_str(
        template_file_name='rotor_internal.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=rotor_keys)


def mdhr_data(potentials, freqs=()):
    """ Writes the string for an auxiliary data file for MESS containing
        potentials and vibrational frequencies of a
        multidimensional hindered rotor, up to four dimensions.

        :param potentials: potential values along torsional modes of rotor
        :type potentials: list(list(float))
        :param freqs: vibrational frequenciess along torsional modes of rotor
        :type freqs: list(list(float))
        :rtype: str
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

    return remove_trail_whitespace(dat_str)


def umbrella_mode(group, plane, ref_atom, potential,
                  remdummy=None, geom=None):
    """ Writes the string that defines the `Umbrella` section for a
        single umbrella mode of a species for a MESS input file by
        formatting input information into strings a filling Mako template.

        :param group: idxs for the atoms of ?
        :type group: list(int)
        :param axis: idxs for the atoms that ?
        :type axis: list(int)
        :param remdummy: list of idxs of dummy atoms for shifting values
        :type remdummy: list(int)
        :param geom: geometry of the species the umbrella mode exists for
        :type geom: list
        :rtype: str
    """

    # Format the sections
    umbr_group = util.format_rotor_key_defs(group, remdummy)
    umbr_plane = util.format_rotor_key_defs(plane, remdummy)
    umbr_npotential, umbr_potential = util.format_rotor_potential(potential)

    # Format the geom
    if geom is not None:
        natom, geom = util.geom_format(geom)
        geom = indent(geom, 4)
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

    return build_mako_str(
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

    return build_mako_str(
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

    return build_mako_str(
        template_file_name='tunnel_sct.mako',
        template_src_path=SPEC_INFO_PATH,
        template_keys=tunnel_keys)
