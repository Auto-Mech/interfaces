""" Write THERMP input file
"""

import os
from mako.template import Template
from thermp_io import util

# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')


def thermp_input(formula, delta_h,
                 enthalpy_temp=0.0, break_temp=1000.0,
                 thermp_file_name='thermp.dat'):
    """ Writes the input file for thermp
    """

    # Get the stoichiometry of all elements to build composition string
    atom_dict = util.get_atom_counts_dict(formula)
    composition_str = ''
    for key, val in atom_dict.items():
        composition_str += '{0}  {1}\n'.format(key, val)
    composition_str = composition_str.rstrip()

    # Create a fill value dictionary
    thermp_keys = {
        'formula': formula,
        'deltaH': delta_h,
        'enthalpyT': enthalpy_temp,
        'breakT': break_temp,
        'composition_str': composition_str
    }

    # Set template name and path for an atom
    template_file_name = 'thermp.mako'
    template_file_path = os.path.join(TEMPLATE_PATH, template_file_name)

    # Build a ProjRot input string
    thermp_str = Template(filename=template_file_path).render(**thermp_keys)

    return thermp_str
