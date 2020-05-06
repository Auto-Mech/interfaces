"""
Writes the energy transfer section of a MESS input file
"""

import os
from mako.template import Template
from mess_io.writer import util


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')
SECTION_PATH = os.path.join(TEMPLATE_PATH, 'sections')


def energy_transfer(exp_factor, exp_power, exp_cutoff,
                    eps1, eps2,
                    sig1, sig2,
                    mass1, mass2):
    """ Writes the energy transfer section of the MESS input file
        :param float exp_factor: Exponent factor
        :param float exp_power: Exponent power
        :param float exp_cutoff: Exponent cutoff
        :param float eps1: Epsilon of Species 1
        :param float eps2: Epsilon of Species 2
        :param float sig1: Sigma of Species 1
        :param float sig2: Sigma of Species 2
        :param float mass1: Mass of Species 1
        :param float mass2: Mass of Species 2
        :return etrans_str: String for section
        :rtype: string
    """

    # Put the values into a string
    epsilon_str = '{0:<10.1f} {1:<10.1f}'.format(eps1, eps2)
    sigma_str = '{0:<10.2f} {1:<10.2f}'.format(sig1, sig2)
    mass_str = '{0:<10.1f} {1:<10.1f}'.format(mass1, mass2)

    # Create dictionary to fill template
    etrans_keys = {
        'exp_factor': exp_factor,
        'exp_power': exp_power,
        'exp_cutoff': exp_cutoff,
        'epsilons': epsilon_str,
        'sigmas': sigma_str,
        'masses': mass_str
    }

    # Set template name and path for the energy transfer section
    template_file_name = 'energy_transfer.mako'
    template_file_path = os.path.join(SECTION_PATH, template_file_name)

    # Build energy transfer string
    etrans_str = Template(filename=template_file_path).render(**etrans_keys)

    return util.remove_trail_whitespace(etrans_str)
