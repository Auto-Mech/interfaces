"""
Reads the outoput of a MESSPF calculation for the
frequencies and ZPEs for torsional modes

Right now, we assume only a single species is in the output
"""

import autoparse.pattern as app
import autoparse.find as apf


def freqs(output_str):
    """ Reads the analytic frequencies for each of the 
        hindered rotors from MESS output file string.

        :param output_str: string of lines of MESS output file
        :type output_str: str
        :return freqs: frequency for each of the rotors
        :rtype: list(float)
    """

    # Pattern for the frequency of a rotor
    pattern = (app.escape('analytic  frequency at minimum[1/cm] =') +
               app.one_or_more(app.SPACE) +
               app.capturing(app.FLOAT))

    # Obtain each frequency from the output string
    tors_freqs = [float(val)
                  for val in apf.all_captures(pattern, output_str)]

    return tors_freqs


def zpves(output_str):
    """ Reads the zero-point energies for each of the 
        hindered rotors from MESS output file string.

        :param output_str: string of lines of MESS output file
        :type output_str: str
        :return zpves: zero-point energy for each of the rotors
        :rtype: list(float)
    """

    # Pattern for the ZPVE of a rotor
    pattern = (app.escape('ground energy [kcal/mol]') +
               app.one_or_more(app.SPACE) +
               '=' +
               app.one_or_more(app.SPACE) +
               app.capturing(app.FLOAT))

    # Obtain each ZPVE from the output string
    tors_zpes = [float(val)
                 for val in apf.all_captures(pattern, output_str)]

    return tors_zpes
