"""
  Tests the varecof_io.writer functions
"""

import varecof_io


def test__tst_writer():
    """ tests varecof_io.writer.input_file.tst
    """

    # Write the tst input string
    nsamp_max = 2000
    nsamp_min = 500
    flux_err = 5
    pes_size = 1
    ener_grid = [0, 20, 1.05, 179]
    amom_grid = [0, 3, 1.10, 50]
    tst_inp_str = varecof_io.writer.input_file.tst(
        nsamp_max, nsamp_min, flux_err, pes_size)
    tst_inp_str2 = varecof_io.writer.input_file.tst(
        nsamp_max, nsamp_min, flux_err, pes_size,
        ener_grid=ener_grid, amom_grid=amom_grid)
    print('\n\ntst.inp (default grid):')
    print(tst_inp_str)
    print('\n\ntst.inp (user-defined grid):')
    print(tst_inp_str2)


# def test__divsur_writer():
#     """ tests varecof_io.writer.input_file.divsur
#     """
#
#     # Write the long range divsur input file
#     rdists = [10.5, 9.0, 8.0, 7.5, 7.0, 6.5, 6.0,
#               5.5, 5.25, 5.0, 4.5, 4.25, 4.0]
#     xyz_pivot1 = [0.0, 0.0, 0.0]
#     xyz_pivot2 = [0.0, 0.0, 0.0]
#     npivot1 = 1
#     npivot2 = 1
#     lr_divsur_inp_str = varecof_io.writer.input_file.divsur(
#         rdists, npivot1, npivot2, xyz_pivot1, xyz_pivot2)
#     print('\n\ndivsur.inp (long-range):')
#     print(lr_divsur_inp_str)
#
#     # Write the short range divsur input files
#     rdists = [4.25, 4.0, 3.75, 3.5, 3.25, 3.0, 2.75]
#     d1dists = [0.05, 0.15, 0.25]
#     p1angs = [85.0]
#     t1angs = [140.0]
#     xyz_pivot1 = [1.0, 2.0, 3.0]
#     xyz_pivot2 = [0.0, 0.0, 0.0]
#     npivot1 = 2
#     npivot2 = 1
#     sr_divsur_inp_str1 = varecof_io.writer.input_file.divsur(
#         rdists, npivot1, npivot2, xyz_pivot1, xyz_pivot2,
#         d1dists=d1dists,
#         p1angs=p1angs,
#         t1angs=t1angs)
#     print('\n\ndivsur.inp (short-range; natoms(frag1) = 1):')
#     print(sr_divsur_inp_str1)
#
#     rdists = [4.25, 4.0, 3.75, 3.5, 3.25, 3.0, 2.75]
#     d1dists = [0.05, 0.15, 0.25]
#     d2dists = [0.05, 0.15, 0.25]
#     p1angs = [85.0]
#     p2angs = [120.0]
#     t1angs = [140.0]
#     t2angs = [165.0]
#     xyz_pivot1 = [1.0, 2.0, 3.0]
#     xyz_pivot2 = [4.0, 5.0, 6.0]
#     npivot1 = 2
#     npivot2 = 2
#     sr_divsur_inp_str2 = varecof_io.writer.input_file.divsur(
#         rdists, npivot1, npivot2, xyz_pivot1, xyz_pivot2,
#         d1dists=d1dists,
#         d2dists=d2dists,
#         p1angs=p1angs,
#         p2angs=p2angs,
#         t1angs=t1angs,
#         t2angs=t2angs)
#     print('\n\ndivsur.inp (short-range; natoms(frag1) >= 2?):')
#     print(sr_divsur_inp_str2)


def test__els_writer():
    """ tests varecof_io.writer.input_file.elec_struct
    """

    # Write the els input string
    exe_path = '/path/to/exe'
    lib_path = '/path/to/lib'
    base_name = 'mol'
    npot = 3
    els_inp_str = varecof_io.writer.input_file.elec_struct(
        exe_path, lib_path, base_name, npot,
        dummy_name='dummy_corr_', lib_name='libcorrpot.so',
        geom_ptt='GEOMETRY_HERE', ene_ptt='molpro_energy')
    print('\n\nels.inp:')
    print(els_inp_str)


def test__structure_writer():
    """ tests varecof_io.writer.input_file.structure
    """

    # Write the structure input string
    geom1 = (('H', (0.0, 0.0, 0.0)),)
    geom2 = (('C', (0.2115677758, -0.4050266480, 0.0238323931)),
             ('H', (0.1997580074, 0.1613210912, -0.9300443271)),
             ('H', (0.6278380682, 0.2349826345, 0.8287405717)),
             ('H', (0.8417991162, -1.3107013202, -0.0916314599)))
    struct_inp_str = varecof_io.writer.input_file.structure(
        geom1, geom2)
    print('\n\nstructure.inp:')
    print(struct_inp_str)


def test__tml_writer():
    """ tests varecof_io.writer.input_file.tml
    """

    # Write the *.tml input string
    memory = 4.0
    basis = 'cc-pvdz'
    wfn = """{uhf,maxit=300;wf,78,1,2}
   {multi,maxit=40;closed,38;occ,40;wf,78,1,0;orbprint,3}
   {multi,maxit=40;closed,37;occ,40;wf,78,1,0;state,2;orbprint,3}"""
    method = '{rs2c, shift=0.25}'
    inf_sep_energy = -654.3210123456
    tml_inp_str = varecof_io.writer.input_file.tml(
        memory, basis, wfn, method, inf_sep_energy)
    print('\n\nmol.tml:')
    print(tml_inp_str)


def test__mcflux_writer():
    """ tests varecof_io.writer.input_file.mc_flux
    """

    mc_flux_inp_str = varecof_io.writer.input_file.mc_flux()
    print('\n\nmc_flux.inp:')
    print(mc_flux_inp_str)


def test__convert_writer():
    """ tests varecof_io.writer.input_file.convert
    """

    # Write the convert.inp input string
    conv_inp_str = varecof_io.writer.input_file.convert()
    print('\n\nconvert.inp:')
    print(conv_inp_str)


if __name__ == '__main__':
    test__tst_writer()
    # test__divsur_writer()
    test__els_writer()
    test__structure_writer()
    test__tml_writer()
    test__mcflux_writer()
    test__convert_writer()
