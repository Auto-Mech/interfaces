"""
Writes MESS input for a monte carlo partition function calculation
"""

import os
from mess_io.writer import util


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')
SECTION_PATH = os.path.join(TEMPLATE_PATH, 'sections')
MONTE_CARLO_PATH = os.path.join(SECTION_PATH, 'monte_carlo')


def mc_species(geom, elec_levels,
               flux_mode_str, data_file_name,
               ground_energy, reference_energy,
               freqs=(), no_qc_corr=False, use_cm_shift=False):
    """ Writes a monte carlo species section

        :param core: `Core` section string in MESS format
        :type core: str
        :param freqs: vibrational frequencies
        :type freqs: list(float)
        :param elec_levels: energy and degeneracy of atom's electronic states
        :type elec_levels: list(float)
        :param hind_rot: string of MESS-format `Rotor` sections for all rotors
        :type hind_rot: str
        :param ground_energy:
        :type ground_energy: float
        :param reference_energy:
        :type reference_energy: float
        :param freqs: vibrational frequencies
        :type freqs: list(float)
        :param no_qc_corr:
        :type no_qc_corr: bool
        :param use_cm_chift:
        :type use_cm_shift: bool
        :rtype: str
    """

    # Format the molecule specification section
    atom_list = util.molec_spec_format(geom)

    # Build a formatted frequencies and elec levels string
    nlevels, levels = util.elec_levels_format(elec_levels)
    if freqs:
        nfreqs, freqs = util.freqs_format(freqs)
        no_qc_corr = True
    else:
        nfreqs = 0

    # Indent various strings string if needed
    flux_mode_str = util.indent(flux_mode_str, 4)

    # Create dictionary to fill template
    monte_carlo_keys = {
        'atom_list': atom_list,
        'flux_mode_str': flux_mode_str,
        'data_file_name': data_file_name,
        'ground_energy': ground_energy,
        'nlevels': nlevels,
        'levels': levels,
        'nfreqs': nfreqs,
        'freqs': freqs,
        'reference_energy': reference_energy,
        'no_qc_corr': no_qc_corr,
        'use_cm_shift': use_cm_shift
    }

    return util.build_mako_str(
        template_file_name='monte_carlo.mako',
        template_src_path=MONTE_CARLO_PATH,
        template_keys=monte_carlo_keys)


def mc_data(geos, enes, grads=(), hessians=()):
    """ Writes the string for an auxliary data file required for
        Monte Carlo calculations in MESS that contains the
        geometries, energies, gradients, and Hessians obtained
        from Monte Carlo sampling of the fluxional modes.

        :param geos: geometries from sampling
        :type geos: list
        :param enes: energies from energies
        :type enes: list(float)
        :param grads: gradients from sampling
        :type grads: list
        :param hessians: Hessians from sampling
        :type hessians: list
        :rtype: str
    """

    if not grads and not hessians:
        assert len(geos) == len(enes)
    elif grads or hessians:
        assert grads and hessians
        assert len(geos) == len(enes) == len(grads) == len(hessians)

    dat_str = ''
    for idx, _ in enumerate(geos):
        idx_str = str(idx+1)
        dat_str += 'Sampling point'+idx_str+'\n'
        dat_str += 'Energy'+'\n'
        dat_str += enes[idx]+'\n'
        dat_str += 'Geometry'+'\n'
        dat_str += geos[idx]+'\n'
        if grads:
            dat_str += 'Gradient'+'\n'
            dat_str += grads[idx]
        if hessians:
            dat_str += 'Hessian'+'\n'
            dat_str += hessians[idx]+'\n'

    return util.remove_trail_whitespace(dat_str)


def fluxional_mode(atom_indices, span=360.0):
    """ Writes the string that defines the `FluxionalMode` section for a
        single fluxional mode (torsion) of a species for a MESS input file by
        formatting input information into strings a filling Mako template.

        :param atom_idxs: idxs of atoms involved in fluxional mode
        :type atom_indices: list(int)
        :param span: range from 0.0 to value that mode was sampled over (deg.)
        :type span: float
        :rtype: str
    """

    # Format the aotm indices string
    atom_indices = util.format_flux_mode_indices(atom_indices)

    # Create dictionary to fill template
    flux_mode_keys = {
        'atom_indices': atom_indices,
        'span': span,
    }

    return util.build_mako_str(
        template_file_name='fluxional_mode.mako',
        template_src_path=MONTE_CARLO_PATH,
        template_keys=flux_mode_keys)
