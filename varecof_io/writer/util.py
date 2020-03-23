"""
 Utility functions for formatting
"""

import os
import subprocess
from qcelemental import constants as qcc
from qcelemental import periodictable as ptab
from automol import geom

# Conversion factors
BOHR2ANG = qcc.conversion_factor('bohr', 'angstrom')

# Obtain the path to a convert struct executable
SRC_PATH = os.path.dirname(os.path.realpath(__file__))


# Utility functions for the structure.inp writer
def determine_struct_type(geo):
    """ determines the linear string
    """

    # Remove dummy atoms
    geo = [coords for coords in geo
           if coords[0] != 'X']

    if geom.is_atom(geo):
        struct_type = 'Monoatomic'
    else:
        if geom.is_linear(geo):
            struct_type = 'Linear'
        else:
            struct_type = 'Nonlinear'

    return struct_type


def format_coords(geo):
    """ format the coords section
    """

    # Get the number of atoms
    natoms = len(geo)

    # Get the geometry information
    symbols = geom.symbols(geo)
    coordinates = geom.coordinates(geo)
    masses = [int(ptab.to_mass(symbol)) if symbol != 'X' else 0
              for symbol in symbols]

    # Build a string with the formatted coordinates string
    if geom.is_atom(geo):
        geo_str = '{0:<4s}{1:<6d}'.format(symbols[0], masses[0])
    else:
        geo_str = '{0} \n'.format(str(natoms))
        for symbol, mass, coords in zip(symbols, masses, coordinates):
            coords = [coord * BOHR2ANG for coord in coords]
            coords_str = '{0:>14.8f}{1:>14.8f}{2:>14.8f}'.format(
                coords[0], coords[1], coords[2])
            geo_str += '{0:<4s}{1:<6d}{2}\n'.format(
                symbol, mass, coords_str)
        # Remove final newline character from the string
        geo_str = geo_str.rstrip()

    return natoms, geo_str


# Utility functions for the tst.inp writer
def format_grids_string(grid, name, units):
    """ format the string using the grids for
        energy and angular momentum for tst.inp file
    """
    grid_str = '{0}_grid{1:>8d}{2:>9d}{3:>11.2f}{4:>7d}'.format(
        name, grid[0], grid[1], grid[2], grid[3])
    grid_str += '     {0:<8s}# {1} grid'.format(units, name)

    return grid_str


def format_faces_string(faces):
    """ format faces keywords
    """
    faces_str = ' '.join((str(val) for val in faces))

    return faces_str


# Utility functions for the divsur.inp writer
def format_values_string(coord, values, conv_factor=1.0):
    """ format the values string for the divsur.inp file
    """
    if values:
        values = ', '.join('{0:.3f}'.format(val * conv_factor)
                           for val in values)
        values_string = '{0} = ({1})'.format(coord, values)
    else:
        values_string = ''

    return values_string


def format_pivot_xyz_string(idx, npivot, xyzp, phi_dependence=False):
    """ format the pivot point xyz
    """

    assert npivot in (1, 2)

    atom_idx = idx
    if idx == 1:
        d_idx = 1
        t_idx = 1
    else:
        d_idx = 2
        t_idx = 2

    if npivot == 1:
        x_val = 'x{0} = {1:.3f}'.format(atom_idx, xyzp[0])
        y_val = '  y{0} = {1:.3f}'.format(atom_idx, xyzp[1])
        z_val = '  z{0} = {1:.3f}'.format(atom_idx, xyzp[2])
        pivot_xyz_string = (x_val + y_val + z_val)
    elif npivot > 1 and not phi_dependence:
        x_val1 = 'x{0} = {1:.3f} + d{2}*cos(t{3})'.format(
            atom_idx, xyzp[0], d_idx, t_idx)
        y_val1 = '  y{0} = {1:.3f} + d{2}*sin(t{3})'.format(
            atom_idx, xyzp[1], d_idx, t_idx)
        z_val1 = '  z{0} = 0.000'.format(
            atom_idx)
        x_val2 = 'x{0} = {1:.3f} - d{2}*cos(t{3})'.format(
            atom_idx+1, xyzp[0], d_idx, t_idx)
        y_val2 = '  y{0} = {1:.3f} - d{2}*sin(t{3})'.format(
            atom_idx+1, xyzp[1], d_idx, t_idx)
        z_val2 = '  z{0} = 0.000'.format(
            atom_idx+1)
        pivot_xyz_string = (x_val1 + y_val1 + z_val1 + '\n' +
                            x_val2 + y_val2 + z_val2)
    else:
        raise NotImplementedError
        # # Not sure if this implementation is any good
        # x_val1 = 'x{0} = {1:.0f} + d{2}*sin(p{0})*cos(t{0})'.format(
        #     atom_idx, xyzp[0], d_idx)
        # y_val1 = '  y{0} = {1:.0f} + d{2}*sin(p{0})*sin(t{0})'.format(
        #     atom_idx, xyzp[1], d_idx)
        # z_val1 = '  z{0} = {1:.0f} + d{2}*cos(p{0})'.format(
        #     atom_idx, xyzp[2], d_idx)
        # x_val2 = 'x{0} = {1:.0f} - d{2}*sin(p{0})*cos(t{0})'.format(
        #     atom_idx+1, xyzp[0], d_idx)
        # y_val2 = '  y{0} = {1:.0f} - d{2}*sin(p{0})*sin(t{0})'.format(
        #     atom_idx+1, xyzp[1], d_idx)
        # z_val2 = '  z{0} = {1:.0f} + d{2}*cos(p{0})'.format(
        #     atom_idx+1, xyzp[2], d_idx)
        # pivot_xyz_string = (x_val1 + y_val1 + z_val1 + '\n' +
        #                     x_val2 + y_val2 + z_val2)

    return pivot_xyz_string


# Utility functions for the species_corr.f correction potential writer
def format_corrpot_dist_string(aidx, bidx, asym, bsym):
    """ set distance string for two atoms for the file
    """
    lasym, lbsym = asym.lower(), bsym.lower()

    dist_string = (
        "      n{0} = {4}\n" +
        "      n{1} = {5}\n" +
        "      r{2}{3} = dsqrt( (x(1,n{1})-x(1,n{0}))**2 +\n" +
        "     x             (x(2,n{1})-x(2,n{0}))**2 +\n" +
        "     x             (x(3,n{1})-x(3,n{0}))**2)\n" +
        "      r{2}{3} = r{2}{3}*0.52917"
    ).format(lasym, lbsym, asym, bsym, aidx, bidx)

    return dist_string


def format_delmlt_string(asym, bsym):
    """ set distance string for two atoms for the file
    """

    delmlt_string = (
        "      delmlt = 1.0d0\n" +
        "      if(r{0}{1}.le.r{0}{1}min) r{0}{1} = r{0}{1}min\n" +
        "      if(r{0}{1}.ge.r{0}{1}max) then\n" +
        "        delmlt = exp(-2.d0*(r{0}{1}-r{0}{1}max))\n" +
        "        r{0}{1}=r{0}{1}max\n" +
        "      endif"
    ).format(asym, bsym)

    return delmlt_string

def format_restrict_dist_string(sym1, sym2, name):
    """ build string that has the distance comparison
    """

    restrict_string = (
        "      if (r{0}{1}.lt.rAB) then\n" +
        "        {2}_corr = 100.0\n" +
        "        return\n" +
        "      endif"
    ).format(sym1, sym2, name)

    return restrict_string


def format_spline_strings(npot, sym1, sym2, species_name):
    """ spline fitting strings
    """

    spline_str = ''
    for i in range(npot):
        if i == 0:
            ifstr = 'if'
        else:
            ifstr = 'else if'
        spline_str += '      {0} (ipot.eq.{1}) then\n'.format(ifstr, str(i+1))
        spline_str += (
            '        call spline(rinp,dv{0},nrin,dvp1,dvpn,dv20)\n' +
            '        call splint(rinp,dv{0},dv20,nrin,r{1}{2},{3})\n'
        ).format(str(i+1), sym1, sym2, species_name+'_corr')
    spline_str += '      endif'

    return spline_str


def divsur_frame_geom_script():
    """ Run the VaReCoF utility script to calculate the fragment
        geometries contained in the divsur.out file
        (only requires the divsur.inp file)
    """
    # conv_cmd = [
    #     os.path.join(SRC_PATH, 'convert_struct'),
    #     'divsur.inp'
    # ]
    conv_cmd = [
        '/lcrc/project/CMRP/amech/VaReCoF/build/convert_struct',
        'divsur.inp'
    ]
    devnull = open(os.devnull, 'w')
    subprocess.check_call(
        conv_cmd, stdout=devnull, stderr=devnull)
