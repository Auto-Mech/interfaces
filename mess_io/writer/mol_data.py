"""
Writes MESS input for a molecule
"""

import os
from mako.template import Template
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

    # Set template name and path for a rigid-rotor core section
    template_file_name = 'core_rigidrotor.mako'
    template_file_path = os.path.join(SPEC_INFO_PATH, template_file_name)

    # Build core section string
    core_rigrot_str = Template(filename=template_file_path).render(**core_keys)

    return core_rigrot_str


def core_multirotor(geom, sym_factor, pot_surf, int_rot,
                    interp_emax=100, quant_lvl_emax=9):
    """ Writes a multi-rotor core section.
    """

    # Format the geometry section
    natom1, geom = util.geom_format(geom)

    # Indent the internal rotor string
    int_rot = util.indent(int_rot, 2)

    # Create dictionary to fill template
    core_keys = {
        'sym_factor': sym_factor,
        'natom': natom,
        'geom': geom,
        'pot_surf': pot_surf,
        'int_rot': int_rot,
        'interp_emax': interp_emax,
        'quant_lvl_emax': quant_lvl_emax
    }

    # Set template name and path for a multi-rotor core section
    template_file_name = 'core_multirotor.mako'
    template_file_path = os.path.join(SPEC_INFO_PATH, template_file_name)

    # Build core section string
    core_mulrot_str = Template(filename=template_file_path).render(**core_keys)

    return core_mulrot_str


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

    # Set template name and path for a phase space core section
    template_file_name = 'core_phasespace.mako'
    template_file_path = os.path.join(SPEC_INFO_PATH, template_file_name)

    # Build core section string
    core_pst_str = Template(filename=template_file_path).render(**core_keys)

    return core_pst_str


def core_rotd(sym_factor, flux_file_name, stoich):
    """ Writes a core section which calls flux files from Rotd/VaReCoF
    """

    # Set values and template based on core type
    core_keys = {
        'sym_factor': sym_factor,
        'flux_file_name': flux_file_name,
        'stoich': stoich
    }

    # Set template name and path for a Rotd core section
    template_file_name = 'core_rotd.mako'
    template_file_path = os.path.join(SPEC_INFO_PATH, template_file_name)

    # Build core section string
    core_rotd_str = Template(filename=template_file_path).render(**core_keys)

    return core_rotd_str


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

    # Set template name and path for a hindered rotor section
    template_file_name = 'rotor_hindered.mako'
    template_file_path = os.path.join(SPEC_INFO_PATH, template_file_name)

    # Build rotor section string
    rotor_hind_str = Template(filename=template_file_path).render(**rotor_keys)

    return rotor_hind_str


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
    natom = 1
    if geom is not None:
        natom, geom = util.geom_format(geom)
        geom = util.indent(geom, 4)

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

    # Set template name and path for a internal rotor section
    template_file_name = 'rotor_internal.mako'
    template_file_path = os.path.join(SPEC_INFO_PATH, template_file_name)

    # Build rotor section string
    rotor_int_str = Template(filename=template_file_path).render(**rotor_keys)

    return rotor_int_str


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

    # Set template name and path for an Eckart tunneling section
    template_file_name = 'tunnel_eckart.mako'
    template_file_path = os.path.join(SPEC_INFO_PATH, template_file_name)

    # Build tunnel section string
    tunnel_str = Template(filename=template_file_path).render(**tunnel_keys)

    return tunnel_str


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

    # Set template name and path for an SCT tunneling section
    template_file_name = 'tunnel_sct.mako'
    template_file_path = os.path.join(SPEC_INFO_PATH, template_file_name)

    # Build tunnel section string
    tunnel_str = Template(filename=template_file_path).render(**tunnel_keys)

    return tunnel_str
