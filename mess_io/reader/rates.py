"""
  Reads the output of a MESS calculation for the
  high-pressure and pressure-dependent rate constants
  corresponding to a given reaction.
"""


def highp_ks(output_str, reactant, product):
    """ Parses the MESS output file string for the rate constants [k(T)]s
        for a single reaction at the high-pressure limit.

        :param output_str: string of lines of MESS output file
        :type output_str: str
        :param reactant: label for the reactant used in the MESS output
        :type reactant: str
        :param product: label for the product used in the MESS output
        :type product: str
        :return rate_constants: all high-P rate constants for the reaction
        :rtype list(float)
    """

    # Build the reaction string found in the MESS output
    reaction = reactant + '->' + product

    # Get the MESS output lines
    mess_lines = output_str.splitlines()

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
            rate_constants = _parse_rate_constants(
                mess_lines, rate_const_block_start, reaction)
            break

    return rate_constants


def pdep_ks(output_str, reactant, product, pressure):
    """ Parses the MESS output file string for the rate constants [k(T,P)]s
        for a single reaction at a given numerical pressure, P.

        :param output_str: string of lines of MESS output file
        :type output_str: str
        :param reactant: label for the reactant used in the MESS output
        :type reactant: str
        :param product: label for the product used in the MESS output
        :type product: str
        :param pressure: pressure that k(T,P)s will be read for
        :return rate_constants: k(T,P)s for the reaction at given pressure
        :rtype list(float)
    """

    # Build the reaction string found in the MESS output
    reaction = reactant + '->' + product

    # Get the MESS output lines
    mess_lines = output_str.splitlines()

    # Find where the block of text where the high-pressure rates exist
    block_str = ('Temperature-Species Rate Tables:')

    rate_constants = []
    for i, line in enumerate(mess_lines):
        if block_str in line:
            for j in range(i, len(mess_lines)):
                if 'Temperature-Pressure Rate Tables' in mess_lines[j]:
                    break
                if reaction in mess_lines[j]:
                    mess_press = mess_lines[j-2].strip().split()[2]
                    if float(mess_press) == pressure:
                        rate_const_block_start = j
                        rate_constants = _parse_rate_constants(
                            mess_lines, rate_const_block_start, reaction)

    return rate_constants


def _parse_rate_constants(mess_lines, block_start, reaction):
    """ Parses specific rate constants from the correct column
        in the MESS output file string.

        :param mess_lines: all of the lines of MESS output
        :type mess_lines: list(str)
        :param block_start: line num corresponding to reaction and pressure
        :type block_start: int
        :param reaction: string matching reaction line in MESS output
        :type reaction: str
        :return rate_constants: all rate constants for the reaction
        :rtype: list(str, float)
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
        rate_constants.append(mess_lines[i].strip().split()[reaction_col])

    # Convert temps and rate constants to floats
    rate_constants = [float(rate_constant)
                      if rate_constant != '***' else rate_constant
                      for rate_constant in rate_constants]

    return rate_constants


def get_temperatures(output_str):
    """ Reads the temperatures from the MESS output file string
        that were used in the master-equation calculation.

        :param output_str: string of lines of MESS output file
        :type output_str: str
        :return temperatures: temperatures in the output
        :rtype: list(float)
        :return temperature_unit: unit of the temperatures in the output
        :rtype: str
    """

    # Get the MESS output lines
    mess_lines = output_str.splitlines()

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
            # else:
            #     temperature_unit = tmp[3]
            #     break

    # Read unit
    for i in range(block_start, len(mess_lines)):
        if 'Temperature =' in mess_lines[i]:
            temperature_unit = mess_lines[i].strip().split()[3]
            break

    return temperatures, temperature_unit


def get_pressures(output_str):
    """ Reads the pressures from the MESS output file string
        that were used in the master-equation calculation.

        :param output_str: string of lines of MESS output file
        :type output_str: str
        :return pressures: pressures in the output
        :rtype: list(str, float)
        :return pressure_unit: unit of the pressures in the output
        :rtype: str
    """

    # Get the MESS output lines
    mess_lines = output_str.splitlines()

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

    # Append high pressure
    pressures.append('high')

    return pressures, pressure_unit


def get_temperatures_input(input_str):
    """ Reads the temperatures from the MESS input file string
        that were used in the master-equation calculation.

        :param input_str: string of lines of MESS input file
        :type input_str: str
        :return temperatures: temperatures in the input
        :rtype: list(float)
        :return temperature_unit: unit of the temperatures in the input
        :rtype: str
    """

    # Get the MESS input lines
    mess_lines = input_str.splitlines()
    for line in mess_lines:
        if 'TemperatureList' in line:
            temperatures = [float(val) for val in line.strip().split()[1:]]
            temperature_unit = line.strip().split('[')[1].split(']')[0]
            break

    return temperatures, temperature_unit


def get_pressures_input(input_str):
    """ Reads the pressures from the MESS input file string
        that were used in the master-equation calculation.

        :param input_str: string of lines of MESS input file
        :type input_str: str
        :return pressures: pressures in the input
        :rtype: list(str, float)
        :return pressure_unit: unit of the pressures in the input
        :rtype: str
    """

    # Get the MESS input lines
    mess_lines = input_str.splitlines()
    for line in mess_lines:
        if 'PressureList' in line:
            pressures = [float(val) for val in line.strip().split()[1:]]
            pressure_unit = line.strip().split('[')[1].split(']')[0]
            break

    # Append high pressure
    pressures.append('high')

    return pressures, pressure_unit
