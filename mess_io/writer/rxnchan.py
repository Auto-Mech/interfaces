"""
Writes MESS input for a molecule
"""

import os
from mako.template import Template
from mess_io.writer import util


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')
SECTION_PATH = os.path.join(TEMPLATE_PATH, 'sections')
RXNCHAN_PATH = os.path.join(SECTION_PATH, 'reaction_channel')


def species(species_label, species_data, zero_energy):
    """ Writes a species section.
    """

    # Indent the string containing all of data for the well
    species_data = util.indent(species_data, 2)

    # Format the precision of the zero energy
    zero_energy = '{0:<8.2f}'.format(zero_energy)

    # Create dictionary to fill template
    species_keys = {
        'species_label': species_label,
        'species_data': species_data,
        'zero_energy': zero_energy
    }

    # Set template name and path for a species
    template_file_name = 'species.mako'
    template_file_path = os.path.join(RXNCHAN_PATH, template_file_name)

    # Build species section string
    species_str = Template(filename=template_file_path).render(**species_keys)

    return util.remove_trail_whitespace(species_str)


def well(well_label, well_data, zero_energy=None):
    """ Writes a well section.
    """

    # Indent the string containing all of data for the well
    well_data = util.indent(well_data, 4)

    # Format the precision of the zero energy
    if zero_energy is not None:
        zero_energy = '{0:<8.2f}'.format(zero_energy)

    # Create dictionary to fill template
    well_keys = {
        'well_label': well_label,
        'well_data': well_data,
        'zero_energy': zero_energy
    }

    # Set template name and path for a well
    template_file_name = 'well.mako'
    template_file_path = os.path.join(RXNCHAN_PATH, template_file_name)

    # Build well section string
    well_str = Template(filename=template_file_path).render(**well_keys)

    return util.remove_trail_whitespace(well_str)


def bimolecular(bimol_label,
                species1_label, species1_data,
                species2_label, species2_data,
                ground_energy):
    """ Writes a Bimolecular section.
    """

    # Indent the string containing all of data for each species
    species1_data = util.indent(species1_data, 4)
    species2_data = util.indent(species2_data, 4)

    # Determine if species is an atom
    isatom1 = util.is_atom_in_str(species1_data)
    isatom2 = util.is_atom_in_str(species2_data)

    # Format the precision of the ground energy
    ground_energy = '{0:<8.2f}'.format(ground_energy)

    # Create dictionary to fill template
    bimol_keys = {
        'bimolec_label': bimol_label,
        'species1_label': species1_label,
        'species1_data': species1_data,
        'isatom1': isatom1,
        'species2_label': species2_label,
        'species2_data': species2_data,
        'isatom2': isatom2,
        'ground_energy': ground_energy
    }

    # Set template name and path for a bimolecular set
    template_file_name = 'bimolecular.mako'
    template_file_path = os.path.join(RXNCHAN_PATH, template_file_name)

    # Build bimolecular section string
    bimol_str = Template(filename=template_file_path).render(**bimol_keys)

    return util.remove_trail_whitespace(bimol_str)


def ts_sadpt(ts_label, reac_label, prod_label, ts_data,
             zero_energy=None, tunnel=''):
    """ Writes a TS section containing only a saddle point
    """

    # Indent the string containing all of data for the saddle point
    ts_data = util.indent(ts_data, 2)
    if tunnel != '':
        tunnel = util.indent(tunnel, 4)

    # Format the precision of the zero energy
    if zero_energy is not None:
        zero_energy = '{0:<8.2f}'.format(zero_energy)

    # Create dictionary to fill template
    ts_sadpt_keys = {
        'ts_label': ts_label,
        'reac_label': reac_label,
        'prod_label': prod_label,
        'ts_data': ts_data,
        'zero_energy': zero_energy,
        'tunnel': tunnel
    }

    # Set template name and path for a TS with only a single saddle point
    template_file_name = 'ts_sadpt.mako'
    template_file_path = os.path.join(RXNCHAN_PATH, template_file_name)

    # Build saddle point string
    sadpt_str = Template(filename=template_file_path).render(**ts_sadpt_keys)

    return util.remove_trail_whitespace(sadpt_str)


def ts_variational(ts_label, reac_label, prod_label, rpath_pt_strs, tunnel=''):
    """ Writes a TS section containing variational information
    """

    # Concatenate all of the variational point strings and indent them
    ts_data = '\n'.join(rpath_pt_strs)
    ts_data = util.indent(ts_data, 4)
    if tunnel != '':
        tunnel = util.indent(tunnel, 4)

    # Create dictionary to fill template
    var_keys = {
        'ts_label': ts_label,
        'reac_label': reac_label,
        'prod_label': prod_label,
        'ts_data': ts_data,
        'tunnel': tunnel
    }

    # Set template name and path for a TS with an variational
    template_file_name = 'ts_var.mako'
    template_file_path = os.path.join(RXNCHAN_PATH, template_file_name)

    # Build transition state with variational string
    var_str = Template(filename=template_file_path).render(**var_keys)

    return util.remove_trail_whitespace(var_str)


def configs_union(mol_data_strs):
    """ Writes a section for a union of species.
    """

    # Add 'End' statment to each of the data strings
    mol_data_strs = [string+'End' for string in mol_data_strs]
    mol_data_strs[-1] += '\n'

    # Concatenate all of the molecule strings
    union_data = '\n'.join(mol_data_strs)
    union_data = util.indent(union_data, 2)

    # Add the tunneling string (seems tunneling goes for all TSs in union)
    # if tunnel != '':
    #     tunnel = util.indent(tunnel, 4)

    # Create dictionary to fill template
    union_keys = {
        'union_data': union_data
    }

    # Set template name and path for a union-of-species
    template_file_name = 'union.mako'
    template_file_path = os.path.join(RXNCHAN_PATH, template_file_name)

    # Build transition state with variational string
    union_str = Template(filename=template_file_path).render(**union_keys)

    return util.remove_trail_whitespace(union_str)
