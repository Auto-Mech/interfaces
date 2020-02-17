"""
Writes MESS input for a monte carlo partition function calculation
"""

import os
from mako.template import Template
from mess_io.writer import util


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')
SECTION_PATH = os.path.join(TEMPLATE_PATH, 'sections')
MONTE_CARLO_PATH = os.path.join(SECTION_PATH, 'monte_carlo')


def monte_carlo(geom, elec_levels,
                flux_mode_str, data_file_name,
                ground_energy, reference_energy,
                freqs=(),
                no_qc_corr=False, use_cm_shift=False):
    """ Writes a monte carlo species section
    """

    # Format the molecule specification section
    atom_list = util.molec_spec_format(geom)

    # Build a formatted frequencies and elec levels string
    nlevels, levels = util.elec_levels_format(elec_levels)
    if freqs:
        nfreqs, freqs = util.freqs_format(freqs)
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

    # Set template name and path for a monte carlo species section
    template_file_name = 'monte_carlo.mako'
    template_file_path = os.path.join(MONTE_CARLO_PATH, template_file_name)

    # Build monte carlo section string
    mc_str = Template(filename=template_file_path).render(**monte_carlo_keys)

    return mc_str


def fluxional_mode(atom_indices, span=360.0):
    """ Writes the string for each fluxional mode
    """

    # Format the aotm indices string
    atom_indices = util.format_flux_mode_indices(atom_indices)

    # Create dictionary to fill template
    flux_mode_keys = {
        'atom_indices': atom_indices,
        'span': span,
    }

    # Set template name and path for a monte carlo species section
    template_file_name = 'fluxional_mode.mako'
    template_file_path = os.path.join(MONTE_CARLO_PATH, template_file_name)

    # Build monte carlo section string
    flux_str = Template(filename=template_file_path).render(**flux_mode_keys)

    return flux_str
