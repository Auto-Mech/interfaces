"""
  Reads the output of a MESS calculation for the
  high-pressure and pressure-dependent rate constants corresponding to
  a given reaction
"""


def highp_ks(output_string, reactant, product):
    """ Reads rate constants for a reaction at the high-pressure limit
        :param str output_string: string of lines for MESS output file
        :param str reactant: label for the reactant used in the MESS output
        :param str product: label for the product used in the MESS output
        :return rate_constants: all rate constants for the reaction
        :rtype: list: str
    """

    # Build the reaction string found in the MESS output
    reaction = reactant + '->' + product

    # Get the MESS output lines
    mess_lines = output_string.splitlines()

    # Find where the block of text where the high-pressure rates exist
    block_str = ('High Pressure Rate Coefficients ' +
                 '(Temperature-Species Rate Tables):')
    for i, line in enumerate(mess_lines):
        if block_str in line:
            block_start = i
            break

    # Get the high-pressure rate constants
    rate_constants = []
    for i in range(block_start, len(mess_lines)):
        if reaction in mess_lines[i]:
            rate_const_block_start = i
            rate_constants = grab_rate_constants(
                mess_lines, rate_const_block_start, reaction)
            break

    return rate_constants


def pdep_ks(output_string, reactant, product, pressure, pressure_unit):
    """ Reads rate constants for a reaction at some pressure
        :param str output_string: string of lines for MESS output file
        :param str reactant: label for the reactant used in the MESS output
        :param str product: label for the product used in the MESS output
        :param str pressure: pressure for which rate constants are desired
        :param str pressure_unit: unit for the pressure in the MESS output
        :return rate_constants: all rate constants for the reaction
        :rtype: list: str
    """

    # Build the reaction string found in the MESS output
    reaction = reactant + '->' + product

    # Get the MESS output lines
    mess_lines = output_string.splitlines()

    # Find where the block of text where the high-pressure rates exist
    block_str = ('Temperature-Species Rate Tables:')
    # pressure_str = 'Pressure = ' + str(pressure) + ' ' + pressure_unit

    for i, line in enumerate(mess_lines):
        if block_str in line:
            for j in range(i, len(mess_lines)):
                if 'Temperature-Pressure Rate Tables' in mess_lines[j]:
                    break
                if reaction in mess_lines[j]:
                    mess_press = mess_lines[j-2].strip().split()[2]
                    if float(mess_press) == pressure:
                        rate_const_block_start = j
                        rate_constants = grab_rate_constants(
                            mess_lines, rate_const_block_start, reaction)

    return rate_constants


def grab_rate_constants(mess_lines, block_start, reaction):
    """ Utility function to grab specific rate constants
        at some pressure for the reaction requested.
        :param list str mess_lines: all of the lines of MESS output
        :param int block_start: line num corresponding to rxn and pressure
        :param reaction: string matching reaction in MESS output
        :return rate_constants: all rate constants for the reaction
        :rtype: list: str
    """

    # Find the column corresponding to the reaction
    reaction_col = 0
    reaction_headers = mess_lines[block_start].strip().split()
    for i, reaction_header in enumerate(reaction_headers):
        if reaction == reaction_header:
            reaction_col = i
            break

    # Parse the following lines and store the constants in a list
    rate_constants = []
    for i in range(block_start+1, len(mess_lines)):
        if mess_lines[i].strip() == '':
            break
        else:
            rate_constants.append(
                mess_lines[i].strip().split()[reaction_col])

    return rate_constants


def get_temperatures(output_string):
    """ Reads the temperatures from the MESS output file corresponding
        to the temperatures used in the master-equation calculation.
        :param str output_string: string of lines for MESS output file
        :return temperatures: temperatures in the output
        :rtype: list: str
        :return temperature_unit: unit the temperatures are reported in
        :rtype: str
    """

    # Get the MESS output lines
    mess_lines = output_string.splitlines()

    # Find the block of lines where the temperatures can be read
    temp_str = 'Pressure-Species Rate Tables:'
    for i, line in enumerate(mess_lines):
        if temp_str in line:
            block_start = i
            break

    # Read the temperatures
    temperatures = []
    for i in range(block_start, len(mess_lines)):
        if 'Temperature =' in mess_lines[i]:
            tmp = mess_lines[i].strip().split()
            temperature_unit = tmp[3]
            if tmp[2] not in temperatures:
                temperatures.append(float(tmp[2]))
            else:
                temperature_unit = tmp[3]
                break

    # Read unit
    for i in range(block_start, len(mess_lines)):
        if 'Temperature =' in mess_lines[i]:
            temperature_unit = mess_lines[i].strip().split()[3]
            break

    return temperatures, temperature_unit


def get_pressures_input(input_string):
    """ Reads pressures from MESS output or input as desired
    """
    # Get the MESS output lines
    mess_lines = input_string.splitlines()
    for line in mess_lines:
        if 'PressureList' in line:
            pressures = [float(val) for val in line.strip().split()[1:]]
            pressure_unit = line.strip().split('[')[1].split(']')[0]
            break

    return pressures, pressure_unit


def get_pressures(output_string):
    """ Reads the pressures from the MESS output file corresponding
        to the pressures used in the master-equation calculation.
        :param str output_string: string of lines for MESS output file
        :return pressures: pressures in the output
        :rtype: list: str
        :return pressure_unit: unit the pressures are reported in
        :rtype: str
    """

    # Get the MESS output lines
    mess_lines = output_string.splitlines()

    # Find the block of lines where the pressures can be read
    pressure_str = 'Pressure-Species Rate Tables:'
    for i, line in enumerate(mess_lines):
        if pressure_str in line:
            block_start = i
            break

    # Read the pressures
    pressures = []
    for i in range(block_start, len(mess_lines)):
        if 'P(' in mess_lines[i]:
            pressure_unit = mess_lines[i].strip().split('(')[1].split(')')[0]
            pressure_start = i+1
            for j in range(pressure_start, len(mess_lines)):
                if 'O-O' in mess_lines[j]:
                    break
                tmp = mess_lines[j].strip().split()
                pressures.append(float(tmp[0]))
            break

    # append high pressure
    pressures.append('high')

    return pressures, pressure_unit
