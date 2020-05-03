""" test the writing of the energy transfer section
"""

import mess_io


def test__energy_trans_writer():
    """ tests writing the section to a file
    """

    # Set the energy transfer parameters for the exponential down model fxn
    exp_factor = 150.0
    exp_power = 50.0
    exp_cutoff = 80.0

    # Set the LJ parameters for the target and bath
    eps1 = 100.0
    eps2 = 200.0
    sig1 = 10.0
    sig2 = 20.0
    mass1 = 15.0
    mass2 = 25.0

    # Use the writer to create a string for the energy transfer section
    energy_trans_section_str = mess_io.writer.energy_transfer(
        exp_factor, exp_power, exp_cutoff,
        eps1, eps2,
        sig1, sig2,
        mass1, mass2)

    # Print the energy transfer section string
    print(energy_trans_section_str)


if __name__ == '__main__':
    test__energy_trans_writer()
