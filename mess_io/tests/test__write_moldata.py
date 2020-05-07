""" Tests the writing of the energy transfer section
"""

import mess_io


def test__core_rigidrotor_writer():
    """ core test
    """

    # Set the base values needed for each of the core sections
    sym_factor = 1.000
    geom = (('O', (1.911401284, 0.16134481659, -0.05448080419)),
            ('N', (4.435924209, 0.16134481659, -0.05448080419)),
            ('N', (6.537299661, 0.16134481659, -0.05448080419)))

    # Use the writer to create a string for each of the core sections
    core_rigrot_str1 = mess_io.writer.mol_data.core_rigidrotor(
        geom=geom,
        sym_factor=sym_factor,
        interp_emax=None)

    # Use the writer to create a string for core sections with add'l keys set
    core_rigrot_str2 = mess_io.writer.mol_data.core_rigidrotor(
        geom=geom,
        sym_factor=sym_factor,
        interp_emax=1500)

    # Print the core string
    print(core_rigrot_str1)
    print('\n')
    print(core_rigrot_str2)


def test__core_multirotor_writer():
    """ core test
    """

    # Set the base values needed for each of the core sections
    sym_factor = 1.000
    geom = (('O', (1.911401284, 0.16134481659, -0.05448080419)),
            ('N', (4.435924209, 0.16134481659, -0.05448080419)),
            ('N', (6.537299661, 0.16134481659, -0.05448080419)))
    pot_surf = 'surf.dat'

    # Write a string for the internal rotor
    group = [11, 10, 9, 8, 7, 6]
    axis = [3, 2, 1]
    symmetry = 1
    rotor_int_str = mess_io.writer.mol_data.rotor_internal(
        group=group,
        axis=axis,
        symmetry=symmetry,
        rotor_id='CH3',
        mass_exp_size=5, pot_exp_size=5,
        hmin=13, hmax=101,
        grid_size=100)

    # Use the writer to create a string for each of the core sections
    core_multirotor_str = mess_io.writer.mol_data.core_multirotor(
        geom=geom,
        sym_factor=sym_factor,
        pot_surf=pot_surf,
        int_rot_str=rotor_int_str,
        interp_emax=100,
        quant_lvl_emax=9)

    # Print the core string
    print(core_multirotor_str)


def test__core_phasespace_writer():
    """ core test
    """

    # Set the values needed for each of the core sections
    sym_factor = 1.000
    geom1 = (('O', (1.911401284, 0.16134481659, -0.05448080419)),
             ('N', (4.435924209, 0.16134481659, -0.05448080419)),
             ('N', (6.537299661, 0.16134481659, -0.05448080419)))
    geom2 = (('O', (1.911401284, 0.16134481659, -0.05448080419)),
             ('N', (4.435924209, 0.16134481659, -0.05448080419)),
             ('N', (6.537299661, 0.16134481659, -0.05448080419)))
    stoich = 'N2O1'

    # Use the writer to create a string for each of the core sections
    core_phasespace_str = mess_io.writer.mol_data.core_phasespace(
        geom1=geom1,
        geom2=geom2,
        sym_factor=sym_factor,
        stoich=stoich,
        pot_prefactor=10, pot_power_exp=6)

    # Print the core string
    print(core_phasespace_str)


def test__core_rotd_writer():
    """ core test
    """

    # Set the values needed for each of the core sections
    sym_factor = 1.000
    stoich = 'N2O1'
    ne_file = 'ne.dat'

    # Use the writer to create a string for each of the core sections
    core_rotd_str = mess_io.writer.mol_data.core_rotd(
        sym_factor=sym_factor,
        flux_file_name=ne_file,
        stoich=stoich)

    # Print the core string
    print(core_rotd_str)


def test__rotor_hindered_writer():
    """ hr test
    """

    # Set the keywords hindered rotor section
    group = [11, 10, 9, 8, 7, 6]
    axis = [3, 2, 1]
    symmetry = 1
    potential = [0.00, 2.91, 9.06, 12.63, 9.97, 3.51,
                 0.03, 3.49, 9.96, 12.63, 9.08, 2.93]

    # Use the writer to create a string for the molecule section
    rot_hind_str = mess_io.writer.mol_data.rotor_hindered(
        group=group,
        axis=axis,
        symmetry=symmetry,
        potential=potential,
        remdummy=None,
        geom=None,
        use_quantum_weight=False)

    # Need tests for other keywords being on

    # Print the hindered rotor section string
    print(rot_hind_str)


def test__rotor_internal_writer():
    """ hr test
    """

    # Set the keywords internal rotor section
    group = [11, 10, 9, 8, 7, 6]
    axis = [3, 2, 1]
    symmetry = 1

    # Use the writer to create a string for the molecule section
    rotor_int_str = mess_io.writer.mol_data.rotor_internal(
        group=group,
        axis=axis,
        symmetry=symmetry,
        rotor_id='CH3',
        mass_exp_size=5, pot_exp_size=5,
        hmin=13, hmax=101,
        grid_size=100)

    # Print the internal rotor string
    print(rotor_int_str)


def test__umbrella_writer():
    """ umbrella test
    """

    # Set the keywords hindered rotor section
    group = [11, 10, 9, 8, 7, 6]
    plane = [3, 2, 1]
    ref_atom = 4
    potential = [0.00, 2.91, 9.06, 12.63, 9.97, 3.51,
                 0.03, 3.49, 9.96, 12.63, 9.08, 2.93]

    # Use the writer to create a string for the molecule section
    umbrella_str = mess_io.writer.mol_data.umbrella_mode(
        group=group,
        plane=plane,
        ref_atom=ref_atom,
        potential=potential,
        remdummy=None,
        geom=None)

    # Need tests for other keywords being on

    # Print the hindered rotor section string
    print(umbrella_str)


def test__tunnel_eckart_writer():
    """ tunnel test
    """

    # Set the values needed for each of the tunnel sections
    imag_freq = 2000
    well_depth1 = 10
    well_depth2 = 20

    # Use the writer to create a string for each of the tunnel sections
    tunnel_eckart_str = mess_io.writer.mol_data.tunnel_eckart(
        imag_freq, well_depth1, well_depth2)

    # Print the Eckart tunnel section
    print(tunnel_eckart_str)


def test__tunnel_sct_writer():
    """ tunnel test
    """

    # Set the values needed for each of the tunnel sections
    imag_freq = 2000
    cutoff_energy = 2500
    tunnel_file = 'imactint.dat'

    # Use the writer to create a string for each of the tunnel sections
    tunnel_sct_str = mess_io.writer.mol_data.tunnel_sct(
        imag_freq, tunnel_file, cutoff_energy=cutoff_energy)

    # Print the SCT tunnel string
    print(tunnel_sct_str)


if __name__ == '__main__':
    test__core_rigidrotor_writer()
    test__core_multirotor_writer()
    test__core_phasespace_writer()
    test__core_rotd_writer()
    test__rotor_hindered_writer()
    test__rotor_internal_writer()
    test__umbrella_writer()
    test__tunnel_eckart_writer()
    test__tunnel_sct_writer()
