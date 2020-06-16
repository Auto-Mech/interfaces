"""
  Functions to write ProjRot input files
"""

import os
from qcelemental import constants as qcc
from ioformat import build_mako_str
from ioformat import remove_trail_whitespace
from projrot_io import util


# Conversion factors
BOHR2ANG = qcc.conversion_factor('bohr', 'angstrom')

# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')


def rpht_input(geoms, grads, hessians,
               saddle_idx=1,
               rotors_str='',
               coord_proj='cartesian',
               proj_rxn_coord=False):
    """ Writes a string for the input file for ProjRot.

        :param geoms: geometry for single species or along a reaction path
        :type geoms: list(list(float))
        :param grads: gradient for single species or along a reaction path
        :type grads: list(list(float))
        :param hessians: Hessian for single species or along a reaction path
        :type hessians: list(list(float))
        :param saddle_idx: idx denoting the saddle point along a reaction path
        :type saddle_idx: int
        :param rotors_str: ProjRot-format string with all the rotor definitions
        :type rotors_str: str
        :param coord_proj: choice of coordinate system to perform projections
        :type coord_proj: str
        :param proj_rxn_coord: whether to project out reaction coordinate
        :type proj_rxn_coord: bool
        :rtype: str
    """

    # Format the molecule info
    data_str = util.write_data_str(geoms, grads, hessians)
    natoms = len(geoms[0])
    # nsteps = len(geoms)
    nrotors = rotors_str.count('pivotA')

    # Check input into the function (really fix calls to not have this)
    if not isinstance(geoms, list):
        geoms = [geoms]
    if not isinstance(grads, list):
        grads = [grads]
    if not isinstance(hessians, list):
        hessians = [hessians]

    nsteps = len(geoms)
    assert nsteps == len(hessians)
    if len(grads) != 0:
        assert len(grads) == nsteps
    assert coord_proj in ('cartesian', 'internal')

    # Create a fill value dictionary
    rpht_keys = {
        'natoms': natoms,
        'nsteps': nsteps,
        'saddle_idx': saddle_idx,
        'coord_proj': coord_proj,
        'prod_rxn_coord': proj_rxn_coord,
        'nrotors': nrotors,
        'rotors_str': rotors_str,
        'data_str': data_str
    }

    return build_mako_str(
        template_file_name='rpht_input.mako',
        template_src_path=TEMPLATE_PATH,
        template_keys=rpht_keys)


def rpht_path_coord_en(coords, energies, bnd1=(), bnd2=()):
    """ Writes a string for the auxiliary input file used for
        ProjRot SCT calculations, which contains information
        along the reaction path.

        :params coords: Values of reaction coordinate along reaction path
        :type coords: list(float)
        :params energies: Energies along reaction path
        :type energies: list(float)
        :params bnd1: values of bond in reactant side
        :type bnd1: list(float)
        :params bnd2: values of bond in product side
        :type bnd2: list(float)
        :rtype: str
    """

    nsteps = len(coords)

    # Check bnd1 and bnd2 lists and build the corresponding string lists
    assert len(bnd1) == len(bnd2)
    assert (bool(bnd1 and bnd2) or bool(not bnd1 and not bnd2))
    bnd_strs = []
    if bnd1 and bnd2:
        for bd1, bd2 in zip(bnd1, bnd2):
            bnd_strs.append('{0:<10.5f}{1:<10.5f}'.format(bd1, bd2))
    else:
        bnd_strs = ['' for i in range(len(coords))]

    # Check that all the lists are not empty and have the same length
    assert all(lst for lst in (coords, energies, bnd_strs))
    assert all(len(lst) == nsteps for lst in (coords, energies, bnd_strs))

    path_str = '{0:<7s}{1:<12s}{2:<10s}{3:<10s}{4:<10s}\n'.format(
        'Point', 'Coordinate', 'Energy', 'Bond1', 'Bond2')
    for i, (crd, ene, bnd_str) in enumerate(zip(coords, energies, bnd_strs)):
        path_str += '{0:<7d}{1:<12.5f}{2:<10.5f}{3:<20s}'.format(
            i+1, crd, ene, bnd_str)
        if i+1 != nsteps:
            path_str += '\n'

    return remove_trail_whitespace(path_str)


def rotors(axis, group, remdummy=None):
    """ Write the sections that defines the rotors section

        :param group: idxs for the atoms of one of the rotational groups
        :type group: list(int)
        :param axis: idxs for the atoms that make up the rotational axis
        :type axis: list(int)
        :param remdummy: list of idxs of dummy atoms for shifting values
        :type remdummy: list(int)
        :rtype str
    """

    # Set up the keywords
    [pivota, pivotb] = axis
    atomsintopa = len(group)
    if remdummy is not None:
        pivota = int(pivota - remdummy[pivota-1])
        pivotb = int(pivotb - remdummy[pivotb-1])
        topaatoms = '  '.join([str(int(val-remdummy[val-1])) for val in group])
    else:
        topaatoms = '  '.join([str(val) for val in group])

    # Build the rotors_str
    rotors_str = '\n{0:<32s}{1:<4d}\n'.format('pivotA', pivota)
    rotors_str += '{0:<32s}{1:<4d}\n'.format('pivotB', pivotb)
    rotors_str += '{0:<32s}{1:<4d}\n'.format('atomsintopA', atomsintopa)
    rotors_str += '{0:<32s}{1}'.format('topAatoms', topaatoms)

    return util.remove_trail_whitespace(rotors_str)
