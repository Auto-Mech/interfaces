"""
Writes the global keyword section of a MESS input file
"""

import os
from mako.template import Template
from qcelemental import constants as qcc
from varecof_io.writer import util


ANG2BOHR = qcc.conversion_factor('angstrom', 'bohr')
RAD2DEG = qcc.conversion_factor('radian', 'degree')

# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')


def tst(nsamp_max, nsamp_min, flux_err, pes_size,
        faces=(0,), faces_symm=1,
        ener_grid=(), amom_grid=()):
    """ Writes the tst.inp file for VaReCoF
        :param int nsamp_max: maximum number of samples
        :param int nsamp_min: minimum number of samples
        :return tst_inp_str: String for tst.inp file
        :rtype: string
    """
    print(faces)
    # Set the energy and angular momentum grids
    if not ener_grid:
        ener_grid = [0, 10, 1.05, 179]
    else:
        assert len(ener_grid) == 4
    if not amom_grid:
        amom_grid = [0, 4, 1.10, 40]
    else:
        assert len(amom_grid) == 4
    ener_grid = util.format_grids_string(ener_grid, 'ener', 'Kelvin')
    amom_grid = util.format_grids_string(amom_grid, 'amom', 'Kelvin')

    # Set the faces
    print(faces)
    faces = util.format_faces_string(faces)

    # Create dictionary to fill template
    tst_keys = {
        'ener_grid': ener_grid,
        'amom_grid': amom_grid,
        'nsamp_max': nsamp_max,
        'nsamp_min': nsamp_min,
        'flux_err': flux_err,
        'pes_size': pes_size,
        'faces': faces,
        'faces_symm': faces_symm
    }

    # Set template name and path for the global keywords section
    template_file_name = 'tst.mako'
    template_file_path = os.path.join(TEMPLATE_PATH, template_file_name)

    # Build tst input string
    tst_str = Template(filename=template_file_path).render(**tst_keys)

    return tst_str


def divsur(rdists,
           npivot1,
           npivot2,
           xyz_pivot1,
           xyz_pivot2,
           frame1=(0, 0, 0, 0),
           frame2=(0, 0, 0, 0),
           r2dists=(),
           d1dists=(), d2dists=(),
           t1angs=(), t2angs=(),
           p1angs=(), p2angs=(),
           phi_dependence=False,
           **conditions
           ):
    """ Writes the divsur.inp file for VaReCoF
        that contains info on the dividing surfaces.
        :param float distances: List of temperatures (in Angstrom)
        :return divsur_inp_str: String for input file
        :rtype: string
    """

    # Format values strings for the coordinates
    # Function returns the empty string if list is empty
    r1_string = util.format_values_string(
        'r1', rdists, conv_factor=ANG2BOHR)
    r2_string = util.format_values_string(
        'r2', rdists, conv_factor=ANG2BOHR)
    d1_string = util.format_values_string(
        'd1', d1dists, conv_factor=ANG2BOHR)
    d2_string = util.format_values_string(
        'd2', d2dists, conv_factor=ANG2BOHR)
    t1_string = util.format_values_string(
        't1', t1angs, conv_factor=RAD2DEG)
    t2_string = util.format_values_string(
        't2', t2angs, conv_factor=RAD2DEG)
    p1_string = util.format_values_string(
        'p1', p1angs, conv_factor=RAD2DEG)
    p2_string = util.format_values_string(
        'p2', p2angs, conv_factor=RAD2DEG)

    # Fromat the frames
    frame1 = ' '.join([str(val) for val in frame1])
    frame2 = ' '.join([str(val) for val in frame2])

    # Write the pivot point coordinates
    idx1 = 1
    idx2 = 1 + npivot1
    if p1angs:
        phi_dependence = True
    pivot_xyz_string1 = util.format_pivot_xyz_string(
        idx1, npivot1, xyz_pivot1, phi_dependence=phi_dependence)
    pivot_xyz_string2 = util.format_pivot_xyz_string(
        idx2, npivot2, xyz_pivot2, phi_dependence=phi_dependence)

    # Calculate the number of cycles
    ncycles = 1
    if r2dists:
        ncycles += 1
    if d1dists:
        ncycles += 1
    if d2dists:
        ncycles += 1
    if p1angs:
        ncycles += 1
    if p2angs:
        ncycles += 1
    if t1angs:
        ncycles += 1
    if t2angs:
        ncycles += 1

    # Determine the string of distance cycles
    if d1dists and d2dists:
        dist_coords_string = 'r11 = r1-(d1+d2)/2\n'
        dist_coords_string += 'r21 = r1-(d1+d2)/2\n'
        dist_coords_string += 'r12 = r2-(d1+d2)/2\n'
        dist_coords_string += 'r22 = r2-(d1+d2)/2'
    elif d1dists and not d2dists:
        dist_coords_string = 'r11 = r1-d1/2\n'
        dist_coords_string += 'r21 = r1-d1/2'
    else:
        dist_coords_string = 'r11 = r1'

    # Build string for conditions
    conditions_string = ''
    nconditions = len(conditions)
    if 'delta_r' in conditions:
        alpha = str(conditions['delta_r'])
        conditions_string += '(r2-r1) < 0.01 + {0}\n'.format(alpha)
        conditions_string += '(r2-r1) > 0.01 + {0}'.format(alpha)

    # Create dictionary to fill template
    divsur_keys = {
        'npivot1': npivot1,
        'npivot2': npivot2,
        'pivot_xyz_string1': pivot_xyz_string1,
        'pivot_xyz_string2': pivot_xyz_string2,
        'frame1': frame1,
        'frame2': frame2,
        'dist_coords_string': dist_coords_string,
        'nconditions': nconditions,
        'conditions_string': conditions_string,
        'ncycles': ncycles,
        'r1_string': r1_string,
        'r2_string': r2_string,
        'd1_string': d1_string,
        'd2_string': d2_string,
        't1_string': t1_string,
        't2_string': t2_string,
        'p1_string': p1_string,
        'p2_string': p2_string,
    }

    # Set template name and path for the global keywords section
    template_file_name = 'divsur.mako'
    template_file_path = os.path.join(TEMPLATE_PATH, template_file_name)

    # Build divsur input string
    divsur_str = Template(filename=template_file_path).render(**divsur_keys)

    return divsur_str


def elec_struct(exe_path, lib_path, base_name, npot,
                dummy_name='dummy_corr_', lib_name='libcorrpot.so',
                geom_ptt='GEOMETRY_HERE', ene_ptt='molpro_energy'):
    """ Writes the electronic structure code input file for VaReCoF
        Currently code only runs with Molpro
        :rtype: string
    """

    # Write the correction potential strings
    pot_path = os.path.join(lib_path, lib_name)
    pot_params_str = ''
    for i in range(npot):
        pot_params_str += '{0:<42s}{1:<8d}\n'.format(base_name+'_corr_', 1)
        pot_params_str += '{0:<42s}{1:<8d}\n'.format('ParameterInteger', i+1)
    pot_params_str += '{0:<42s}{1:<8d}\n'.format(dummy_name, 1)

    # Create dictionary to fill template
    els_keys = {
        'exe_path': exe_path,
        'geom_ptt': geom_ptt,
        'ene_ptt': ene_ptt,
        'base_name': base_name,
        'pot_path': pot_path,
        'pot_params_str': pot_params_str
    }

    # Set template name and path for the global keywords section
    template_file_name = 'els.mako'
    template_file_path = os.path.join(TEMPLATE_PATH, template_file_name)

    # Build tst input string
    els_str = Template(filename=template_file_path).render(**els_keys)

    return els_str


def structure(geo1, geo2):
    """ Writes the structure input file for VaReCoF
        :rtype: string
    """

    # Determine linearity of molecule
    struct_type1 = util.determine_struct_type(geo1)
    struct_type2 = util.determine_struct_type(geo2)

    # Format the coordinates of the geoetry
    natoms1, coords1 = util.format_coords(geo1)
    natoms2, coords2 = util.format_coords(geo2)

    # Create dictionary to fill template
    struct_keys = {
        'struct_type1': struct_type1,
        'natoms1': natoms1,
        'coords1': coords1,
        'struct_type2': struct_type2,
        'natoms2': natoms2,
        'coords2': coords2,
    }

    # Set template name and path for the global keywords section
    template_file_name = 'struct.mako'
    template_file_path = os.path.join(TEMPLATE_PATH, template_file_name)

    # Build structure input string
    struct_str = Template(filename=template_file_path).render(**struct_keys)

    return struct_str


def tml(memory, basis, wfn, method, inf_sep_energy):
    """ writes the tml file used as the template for the electronic structure
        calculation
        currently, we assume the use of molpro
        in particular: method and wfn assume molpro input card structure
    """

    # convert the memory
    memory_mw = int(memory * (1024.0 / 8.0))

    # make the infinite seperation energy positive
    inf_sep_energy *= -1.0

    # Create dictionary to fill template
    tml_keys = {
        'memory': memory_mw,
        'basis': basis,
        'method': method,
        'wfn': wfn,
        'inf_sep_energy': inf_sep_energy
    }

    # Set template name and path for the tml input file string
    template_file_name = 'tml.mako'
    template_file_path = os.path.join(TEMPLATE_PATH, template_file_name)

    # Build structure input string
    tml_str = Template(filename=template_file_path).render(**tml_keys)

    return tml_str


def mc_flux():
    """ Writes the mc_flux.inp file
        :return mc_flux_inp_str: String for input file
        :rtype: string
    """
    mc_flux_inp_str = 'MultiInputFile          tst.inp\n'
    mc_flux_inp_str += 'OutputFile              mc_flux.out\n'
    mc_flux_inp_str += 'Face                    0\n'
    mc_flux_inp_str += 'ElectronicSurface       0'
    return mc_flux_inp_str


def convert():
    """ Writes the convert.inp file
        :return convert_inp_str: String for input file
        :rtype: string
    """
    convert_inp_str = 'MultiInputFile    tst.inp'
    return convert_inp_str
