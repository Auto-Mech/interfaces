""" test the writing of the global keyword section for reactions and messpf
"""

import mess_io.writer


def test__global_reaction():
    """ tests writing the section to a file for reactions
    """

    # Set the temperatures and pressures in a list
    temps = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0]
    pressures = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]

    # Use the writer to create a string for the global keyword section for rxns
    global_reaction_str = mess_io.writer.global_reaction(
        temperatures=temps,
        pressures=pressures)

    # Print the global section string
    print(global_reaction_str)


def test__global_pf():
    """ tests writing the section to a file for messpf
    """

    # Set the temperatures and pressures in a list
    temperatures = []
    temp_step = 100
    ntemps = 30
    rel_temp_inc = 0.001
    atom_dist_min = 0.6

    # Use the writer to create a string for the messpf global keyword section
    global_pf_str = mess_io.writer.global_pf(
        temperatures=temperatures,
        temp_step=temp_step,
        ntemps=ntemps,
        rel_temp_inc=rel_temp_inc,
        atom_dist_min=atom_dist_min)

    # Print the global section string
    print(global_pf_str)


if __name__ == '__main__':
    test__global_reaction()
    test__global_pf()
