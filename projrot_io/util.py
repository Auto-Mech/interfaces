"""
  Additional functions for formatting information for MESS strings
"""

import numpy
from qcelemental import constants as qcc
from qcelemental import periodictable as ptab
from ioformat import remove_trail_whitespace


BOHR2ANG = qcc.conversion_factor('bohr', 'angstrom')


def write_data_str(geoms, grads, hessians):
    """ Writes a string containing the geometry, gradient, and Hessian
        for either a single species or points along a reaction path
        that is formatted appropriately for the ProjRot input file.

        :param geoms: geometries
        :type geoms: list
        :param grads: gradients
        :type grads: list
        :param hessians: Hessians
        :type hessians: list
        :rtype: str
    """

    if not isinstance(geoms, list):
        geoms = [geoms]
    if not isinstance(grads, list):
        grads = [grads]
    if not isinstance(hessians, list):
        hessians = [hessians]
    nsteps = len(geoms)

    data_str = ''
    for i, (geo, grad, hess) in enumerate(zip(geoms, grads, hessians)):
        data_str += 'Step    {0}\n'.format(str(i+1))
        data_str += 'geometry\n'
        data_str += _format_geom_str(geo)
        data_str += 'gradient\n'
        data_str += _format_grad_str(geo, grad)
        data_str += 'Hessian\n'
        data_str += _format_hessian_str(hess)
        if i != nsteps-1:
            data_str += '\n'

    return remove_trail_whitespace(data_str)


def _format_geom_str(geom):
    """ Formats the geometry into a string used for the ProjRot input file.

        :param geoms: geometries (Angstrom)
        :type geoms: list
        :rtype: str
    """

    # Format the strings for the xyz coordinates
    geom_str = ''
    for i, (sym, coords) in enumerate(geom):
        anum = int(ptab.to_Z(sym))
        coords = [coord * BOHR2ANG for coord in coords]
        coords_str = '{0:>14.8f}{1:>14.8f}{2:>14.8f}'.format(
            coords[0], coords[1], coords[2])
        geom_str += '{0:2d}{1:4d}{2:4d}{3}\n'.format(
            i+1, anum, 0, coords_str)

    return remove_trail_whitespace(geom_str)


def _format_grad_str(geom, grad):
    """ Formats the gradient into a string used for the ProjRot input file.

        :param geom: geometries (Angstrom)
        :type geom: list
        :param grads: gradients (Eh/Bohr)
        :type grads: list
        :rtype: str
    """

    atom_list = []
    for i, (sym, _) in enumerate(geom):
        atom_list.append(int(ptab.to_Z(sym)))

    # Format the strings for the xyz gradients
    full_grads_str = ''
    for i, grads in enumerate(grad):
        grads_str = '{0:>14.8f}{1:>14.8f}{2:>14.8f}'.format(
            grads[0], grads[1], grads[2])
        full_grads_str += '{0:2d}{1:4d}{2}\n'.format(
            i+1, atom_list[i], grads_str)

    return remove_trail_whitespace(full_grads_str)


def _format_hessian_str(hess):
    """ Formats the Hessian into a string used for the ProjRot input file.

        :param hess: hessians (Eh/Bohr^2)
        :type hess: list
        :rtype: str
    """

    # Format the Hessian
    hess = numpy.array(hess)
    nrows = numpy.shape(hess)[0]
    ncols = numpy.shape(hess)[1]

    if nrows % 5 == 0:
        nchunks = nrows // 5
    else:
        nchunks = (nrows // 5) + 1

    hess_str = '   ' + '    '.join([str(val) for val in range(1, 6)]) + '\n'
    cnt = 0
    while cnt+1 <= nchunks:
        for i in range(nrows):
            col_tracker = 1
            if i >= 5*cnt:
                hess_str += '{0}'.format(str(i+1))
                for j in range(5*cnt, ncols):
                    if i >= j:
                        if col_tracker <= 5:
                            hess_str += '  {0:5.8f}'.format(hess[i][j])
                            col_tracker += 1
                            if col_tracker == 6:
                                hess_str += '\n'
                        else:
                            continue
                    elif i < j and col_tracker != 6:
                        hess_str += '\n'
                        break
                    else:
                        break
            if i+1 == nrows and cnt+1 < nchunks-1:
                val_str = '     '.join(
                    [str(val)
                     for val in range(5*(cnt+1) + 1, 5*(cnt+1) + 6)])
                hess_str += '    ' + val_str + '\n'
            if i+1 == nrows and cnt+1 == nchunks-1:
                val_str = '     '.join(
                    [str(val)
                     for val in range(5*(cnt+1) + 1, nrows+1)])
                hess_str += '    ' + val_str + '\n'
        cnt += 1

    return remove_trail_whitespace(hess_str)
