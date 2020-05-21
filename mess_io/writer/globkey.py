"""
Writes the global keyword section of a MESS input file
"""

import os
from ioformat import build_mako_str


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')
SECTION_PATH = os.path.join(TEMPLATE_PATH, 'sections')


def global_reaction(temperatures, pressures):
    """ Writes the global keywords section of the MESS input file by
        formatting input information into strings a filling Mako template.

        :param temperatures: List of temperatures (in K)
        :type temperatures: float
        :param pressures: List of pressures (in atm)
        :type pressures: float
        :return global_str: String for section
        :rtype: string
    """

    # Format temperature and pressure lists
    temperature_list = '  '.join(str(val) for val in temperatures)
    pressure_list = '  '.join(str(val) for val in pressures)

    # Create dictionary to fill template
    globrxn_keys = {
        'temperatures': temperature_list,
        'pressures': pressure_list
    }

    return build_mako_str(
        template_file_name='global_reaction.mako',
        template_src_path=SECTION_PATH,
        template_keys=globrxn_keys)


def global_pf(temperatures=(),
              temp_step=100, ntemps=30,
              rel_temp_inc=0.001, atom_dist_min=0.6):
    """ Writes the global keywords section of the MESS input file by
        formatting input information into strings a filling Mako template.

        :param temperatures: List of temperatures (in K)
        :type temperatures: list(float)
        :param temp_step: temperature step (in K)
        :type temp_step: float
        :param ntemps: number of temperature values on grid
        :type ntemps: int
        :param rel_temp_inc: increment for temps
        :type rel_temp_inc: float
        :param atom_dist_min: cutoff for atom distances (Angstrom)
        :type atom_dist_min: float
        :return global_pf_str: string for section
        :rtype: string
    """

    if temperatures:
        temperature_list = '  '.join(str(val) for val in temperatures)
        temp_step = None
        ntemps = None
    else:
        temperature_list = ''

    # Create dictionary to fill template
    globpf_keys = {
        'temperatures': temperature_list,
        'temp_step': temp_step,
        'ntemps': ntemps,
        'rel_temp_inc': rel_temp_inc,
        'atom_dist_min': atom_dist_min
    }

    return build_mako_str(
        template_file_name='global_pf.mako',
        template_src_path=SECTION_PATH,
        template_keys=globpf_keys)
