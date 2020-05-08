"""
Writes the global keyword section of a MESS input file
"""

import os
from mako.template import Template
from mess_io.writer import util


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')
SECTION_PATH = os.path.join(TEMPLATE_PATH, 'sections')


def global_reaction(temperatures, pressures):
    """ Writes the global keywords section of the MESS input file
        :param float temperatures: List of temperatures (in K)
        :param float pressures: List of pressures (in atm)
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

    return util.build_mako_str(
        template_file_name='global_reaction.mako',
        template_src_path=SECTION_PATH,
        template_keys=globrxn_keys)


def global_pf(temperatures=(),
              temp_step=100, ntemps=30,
              rel_temp_inc=0.001, atom_dist_min=0.6):
    """ Writes the global keywords section of the MESS input file
        :param list float temperatures: List of temperatures (in K)
        :param float temp_step: temperature step (in K)
        :param ntemps: number of temperature values on grid
        :param float rel_temp_inc: increment for temps
        :param float atom_dist_min: cutoff for atom distances (Angstrom)
        :return global_pf_str: String for section
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

    return util.build_mako_str(
        template_file_name='global_pf.mako',
        template_src_path=SECTION_PATH,
        template_keys=globpf_keys)
