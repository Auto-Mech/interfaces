"""
Writes the energy transfer section of a MESS input file
"""

import os
from ioformat import build_mako_str


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')
SECTION_PATH = os.path.join(TEMPLATE_PATH, 'sections')


def energy_transfer(exp_factor, exp_power, exp_cutoff,
                    eps1, eps2,
                    sig1, sig2,
                    mass1, mass2):
    """ Writes the energy transfer section of the MESS input file by
        formatting input information into strings a filling Mako template.

        :param exp_factor: 300 K energy-down value for collision model (cm-1)
        :type exp_factor: float
        :param exp_power: n, for [energy-down * (T/300K)^n] for collision model
        :type exp_power: float
        :param exp_cutoff: cutoff for assuming transition probability is zero
        :type exp_cutoff: float
        :param eps1: Lennard-Jones epsilon parameter of species 1 (K to cm-1)
        :type eps1: float
        :param eps2: Lennard-Jones epsilon parameter of species 2 (K to cm-1)
        :type eps2: float
        :param sig1: Lennard-Jones sigma parameter of species 1 (Angstrom)
        :type sig1: float
        :param sig2: Lennard-Jones sigma parameter of species 2 (Angstrom)
        :type sig2: float
        :param mass1: mass of Species 1 (amu)
        :type mass1: float
        :param mass2: mass of Species 2 (amu)
        :type mass2: float
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

    return build_mako_str(
        template_file_name='energy_transfer.mako',
        template_src_path=SECTION_PATH,
        template_keys=etrans_keys)
